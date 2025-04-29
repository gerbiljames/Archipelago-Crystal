import copy
import os
from typing import TYPE_CHECKING

import bsdiff4

from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension
from . import FreeFlyLocation
from .data import data, MiscOption
from .items import item_const_name_to_id
from .options import Route32Condition, UndergroundsRequirePower, RequireItemfinder, Goal, Route2Access, \
    BlackthornDarkCaveAccess, NationalParkAccess, KantoAccessCondition, Route3Access
from .utils import convert_to_ingame_text, write_bytes, replace_map_tiles

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


class PokemonCrystalAPPatchExtension(APPatchExtension):
    game = "Pokemon Crystal"

    @staticmethod
    def apply_bsdiff4(caller: APProcedurePatch, rom: bytes, patch: str):
        revision_address = data.rom_addresses["AP_ROM_Revision"]
        rom_bytes = bytearray(rom)
        if rom_bytes[revision_address] == 1:
            if "basepatch11.bsdiff4" not in caller.files:
                raise Exception("This patch was generated without support for Pokemon Crystal V1.1 ROM. "
                                "Please regenerate with a newer APWorld version or use a V1.0 ROM")
            return bsdiff4.patch(rom, caller.get_file("basepatch11.bsdiff4"))
        return bsdiff4.patch(rom, caller.get_file(patch))


class PokemonCrystalProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Pokemon Crystal"
    hash = "9f2922b235a5eeb78d65594e82ef5dde"
    patch_file_ending = ".apcrystal"
    result_file_ending = ".gbc"

    procedure = [
        ("apply_bsdiff4", ["basepatch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def generate_output(world: "PokemonCrystalWorld", output_directory: str, patch: PokemonCrystalProcedurePatch) -> None:
    option_bytes = bytearray(max([item.option_byte_index for item in data.game_settings.values()]) + 1)

    for setting_name, setting in data.game_settings.items():
        option_selection = world.options.game_options.get(setting_name, None)
        setting.set_option_byte(option_selection, option_bytes)

    write_bytes(patch, option_bytes, data.rom_addresses["AP_Setting_DefaultOptions"])

    item_texts = []
    for location in world.multiworld.get_locations(world.player):
        if location.address is None:
            continue

        if not world.options.remote_items and location.item and location.item.player == world.player:
            item_id = location.item.code
            item_id = item_id - 256 if item_id > 256 else item_id
            write_bytes(patch, [item_id], location.rom_address)
        else:
            # for in game text
            item_flag = location.address
            player_name = world.multiworld.player_name[location.item.player].upper()
            item_name = location.item.name.upper()
            item_texts.append([player_name, item_name, item_flag])

            write_bytes(patch, [item_const_name_to_id("AP_ITEM")], location.rom_address)

    # table has format: location id (2 bytes), string address (2 bytes), string bank (1 byte),
    # and is terminated by 0xFF
    item_name_table_length = len(item_texts) * 5 + 1
    item_name_table_adr = data.rom_addresses["AP_ItemText_Table"]

    # strings are 16 chars each, plus a terminator byte,
    # this gives every pair of item + player names a size of 34 bytes
    item_name_bank1 = item_name_table_adr + item_name_table_length
    item_name_bank1_length = data.rom_addresses["AP_ItemText_Bank1_End"] - item_name_bank1
    item_name_bank1_capacity = int(item_name_bank1_length / 34)

    item_name_bank2 = data.rom_addresses["AP_ItemText_Bank2"]
    item_name_bank2_length = data.rom_addresses["AP_ItemText_Bank2_End"] - item_name_bank2
    item_name_bank2_capacity = int(item_name_bank2_length / 34)

    for i, text in enumerate(item_texts):
        # truncate if too long
        player_text = convert_to_ingame_text(text[0])[:16]
        # pad with terminator byte to keep alignment
        player_text += [0x50] * (17 - len(player_text))
        item_text = convert_to_ingame_text(text[1])[:16]
        item_text.append(0x50)
        # bank 1
        bank = 0x75
        table_offset_adr = item_name_table_adr + i * 5

        if i >= item_name_bank1_capacity + item_name_bank2_capacity:
            # if we somehow run out of capacity in both banks, just finish the table and break,
            # there is a fallback string in the ROM, so it should handle this gracefully.
            write_bytes(patch, [0xFF], item_name_table_adr + table_offset_adr)
            print("oopsie")
            break
        if i + 1 < item_name_bank1_capacity:
            text_offset = i * 34
            text_adr = item_name_bank1 + text_offset
        else:
            # bank 2
            bank = 0x76
            text_offset = (i + 1 - item_name_bank1_capacity) * 34
            text_adr = item_name_bank2 + text_offset
        write_bytes(patch, player_text + item_text, text_adr)
        # get the address within the rom bank (0x4000 - 0x7FFF)
        text_bank_adr = (text_adr % 0x4000) + 0x4000
        write_bytes(patch, text[2].to_bytes(2, "big"), table_offset_adr)
        write_bytes(patch, text_bank_adr.to_bytes(2, "little"), table_offset_adr + 2)
        write_bytes(patch, [bank], table_offset_adr + 4)
    write_bytes(patch, [0xFF], item_name_table_adr + item_name_table_length - 1)

    world.finished_level_scaling.wait()

    if world.options.randomize_static_pokemon:
        for _static_name, pkmn_data in world.generated_static.items():
            pokemon_id = data.pokemon[pkmn_data.pokemon].id
            for address in pkmn_data.addresses:
                cur_address = data.rom_addresses[address] + 1
                write_bytes(patch, [pokemon_id], cur_address)
            if pkmn_data.level_address is not None:
                if pkmn_data.level_type in ["givepoke", "loadwildmon"]:
                    write_bytes(patch, [pkmn_data.level], data.rom_addresses[pkmn_data.level_address] + 2)
                elif pkmn_data.level_type == "custom":
                    write_bytes(patch, [pkmn_data.level], data.rom_addresses[pkmn_data.level_address] + 1)

    if world.options.randomize_trades:
        trade_table_address = data.rom_addresses["AP_Setting_TradeTable"]
        for trade in world.generated_trades:
            trade_address = trade_table_address + (trade.index * 32)  # each trade record is 32 bytes
            requested = data.pokemon[trade.requested_pokemon].id
            write_bytes(patch, [requested], trade_address + 1)

            received = data.pokemon[trade.received_pokemon].id
            write_bytes(patch, [received], trade_address + 2)

            write_bytes(patch, [trade.requested_gender], trade_address + 30)

            item_id = item_const_name_to_id(trade.held_item)
            write_bytes(patch, [item_id], trade_address + 16)

    if world.options.randomize_starters:
        for j, pokemon in enumerate(["CYNDAQUIL_", "TOTODILE_", "CHIKORITA_"]):
            pokemon_id = data.pokemon[world.generated_starters[j][0]].id
            for i in range(1, 5):
                cur_address = data.rom_addresses["AP_Starter_" + pokemon + str(i)] + 1
                write_bytes(patch, [pokemon_id], cur_address)
                if i == 4:
                    helditem = item_const_name_to_id(world.generated_starter_helditems[j])
                    write_bytes(patch, [helditem], cur_address + 2)

    if world.options.randomize_wilds:
        for grass_name, grass_encounters in world.generated_wild.grass.items():
            cur_address = data.rom_addresses["AP_WildGrass_" + grass_name] + 3
            for i in range(3):  # morn, day, nite
                for encounter in grass_encounters:
                    pokemon_id = data.pokemon[encounter.pokemon].id
                    write_bytes(patch, [encounter.level, pokemon_id], cur_address)
                    cur_address += 2

        for water_name, water_encounters in world.generated_wild.water.items():
            cur_address = data.rom_addresses["AP_WildWater_" + water_name] + 1
            for encounter in water_encounters:
                pokemon_id = data.pokemon[encounter.pokemon].id
                write_bytes(patch, [encounter.level, pokemon_id], cur_address)
                cur_address += 2

        for fish_name, fish_data in world.generated_wild.fish.items():
            cur_address = data.rom_addresses["AP_FishMons_" + fish_name]
            for rod_type in [fish_data.old, fish_data.good, fish_data.super]:
                for i, encounter in enumerate(rod_type):
                    if world.options.normalize_encounter_rates:
                        # fishing encounter rates are stored as an increasing fraction of 255
                        encounter_rate = int(((i + 1) / len(rod_type)) * 255)
                        write_bytes(patch, [encounter_rate], cur_address)
                    cur_address += 1
                    pokemon_id = data.pokemon[encounter.pokemon].id
                    write_bytes(patch, [pokemon_id, encounter.level], cur_address)
                    cur_address += 2

        for tree_name, tree_data in world.generated_wild.tree.items():
            cur_address = data.rom_addresses["TreeMonSet_" + tree_name]
            for rarity in [tree_data.common, tree_data.rare]:
                for i, encounter in enumerate(rarity):
                    if world.options.normalize_encounter_rates:
                        # headbutt encounter rates are stored as individual percentages
                        encounter_rate = int(1 / len(rarity) * 100)
                        if i + 1 == len(rarity):
                            # casting to int means the total percentages will not sum to 100,
                            # this accounts for the discrepancy
                            encounter_rate = 100 - (i * encounter_rate)
                        write_bytes(patch, [encounter_rate], cur_address)
                    cur_address += 1
                    pokemon_id = data.pokemon[encounter.pokemon].id
                    write_bytes(patch, [pokemon_id, encounter.level], cur_address)
                    cur_address += 2

        wooper_sprite_address = data.rom_addresses["AP_Setting_Intro_Wooper_1"] + 1
        wooper_cry_address = data.rom_addresses["AP_Setting_Intro_Wooper_2"] + 1
        wooper_id = data.pokemon[world.generated_wooper].id
        write_bytes(patch, [wooper_id], wooper_sprite_address)
        write_bytes(patch, [wooper_id], wooper_cry_address)

    if world.options.normalize_encounter_rates:
        # list of percentage, byte offset for encounter tables (byte offsets are index * 2)
        grass_prob_table = [f(x) for x in range(7) for f in (lambda x: int((x + 1) / 7 * 100), lambda x: x * 2)]
        water_prob_table = [f(x) for x in range(3) for f in (lambda x: int((x + 1) / 3 * 100), lambda x: x * 2)]
        write_bytes(patch, grass_prob_table, data.rom_addresses["AP_Prob_GrassMon"])
        write_bytes(patch, water_prob_table, data.rom_addresses["AP_Prob_WaterMon"])

    if world.options.randomize_berry_trees:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_BerryTrees"] + 1)
        # 0xC9 = ret
        write_bytes(patch, [0xC9], data.rom_addresses["AP_Setting_FruitTreesReset"])

    if world.options.randomize_move_values or world.options.randomize_move_types:
        for move_name, move in world.generated_moves.items():  # effect modification is also possible but not included
            if move_name in ["NO_MOVE", "CURSE"]:
                continue
            if world.options.randomize_move_types:
                address = data.rom_addresses["AP_MoveData_Type_" + move_name]
                move_type_id = [data.type_ids[move.type]]
                write_bytes(patch, move_type_id, address)  # uses same type id conversion that pkmn type randomizer
            if world.options.randomize_move_values > 0:
                address = data.rom_addresses["AP_MoveData_Power_" + move_name]
                write_bytes(patch, [move.power], address)  # power 20-150
                address = data.rom_addresses["AP_MoveData_PP_" + move_name]
                write_bytes(patch, [move.pp], address)  # 5-40 PP
                if world.options.randomize_move_values == 3:
                    address = data.rom_addresses["AP_MoveData_Accuracy_" + move_name]
                    acc = int(move.accuracy * 255 / 100)
                    write_bytes(patch, [acc], address)  # accuracy 30-100

    for pkmn_name, pkmn_data in world.generated_pokemon.items():
        if world.options.randomize_types.value:
            address = data.rom_addresses["AP_Stats_Types_" + pkmn_name]
            pkmn_types = [pkmn_data.types[0], pkmn_data.types[-1]]
            type_ids = [data.type_ids[pkmn_types[0]], data.type_ids[pkmn_types[1]]]
            write_bytes(patch, type_ids, address)

        if world.options.randomize_base_stats.value:
            address = data.rom_addresses["AP_Stats_Base_" + pkmn_name]
            write_bytes(patch, pkmn_data.base_stats, address)

        if world.options.randomize_learnsets.value:
            address = data.rom_addresses["AP_Attacks_" + pkmn_name]
            for move in pkmn_data.learnset:
                move_id = data.moves[move.move].rom_id
                write_bytes(patch, [move.level, move_id], address)
                address += 2

        if pkmn_name in world.generated_palettes:
            palettes = world.generated_palettes[pkmn_name]
            address = data.rom_addresses["AP_Stats_Palette_" + pkmn_name]
            write_bytes(patch, palettes, address)

        tm_bytes = [0, 0, 0, 0, 0, 0, 0, 0]
        for tm in pkmn_data.tm_hm:
            tm_num = data.tmhm[tm].tm_num
            tm_bytes[int((tm_num - 1) / 8)] |= 1 << (tm_num - 1) % 8
        tm_address = data.rom_addresses["AP_Stats_TMHM_" + pkmn_name]
        write_bytes(patch, tm_bytes, tm_address)

    for trainer_name, trainer_data in world.generated_trainers.items():
        address = data.rom_addresses["AP_TrainerParty_" + trainer_name]
        address += trainer_data.name_length + 1  # skip name and type
        for pokemon in trainer_data.pokemon:
            pokemon_data = [pokemon.level, data.pokemon[pokemon.pokemon].id]
            if pokemon.item is not None:
                item_id = item_const_name_to_id(pokemon.item)
                pokemon_data.append(item_id)
            for move in pokemon.moves:
                move_id = data.moves[move].rom_id
                pokemon_data.append(move_id)
            write_bytes(patch, pokemon_data, address)
            address += len(pokemon_data)

    if world.options.randomize_tm_moves.value:
        tm_moves = [tm_data.move_id for _name, tm_data in world.generated_tms.items()]
        address = data.rom_addresses["AP_Setting_TMMoves"]
        write_bytes(patch, tm_moves, address)

    if world.options.enable_mischief:
        if MiscOption.FuchsiaGym.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_FuchsiaTrainers"] + 1
            write_bytes(patch, [0x0a], address + 2)  # spin speed
            for c in world.generated_misc.fuchsia_gym_trainers:
                write_coords = [c[1] + 4, c[0] + 4]
                write_bytes(patch, write_coords, address)
                address += 13

        if MiscOption.SaffronGym.value in world.generated_misc.selected:
            for pair in world.generated_misc.saffron_gym_warps.pairs:
                addresses = [data.rom_addresses["AP_Misc_SaffronGymWarp_" + warp] + 2 for warp in pair]
                ids = [world.generated_misc.saffron_gym_warps.warps[warp].id for warp in pair]
                write_bytes(patch, [ids[1]], addresses[0])  # reverse ids
                write_bytes(patch, [ids[0]], addresses[1])

        if MiscOption.EcruteakGym.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_Ecruteak_Gym_Warp"]
            write_bytes(patch, [2, 5], address)

        if MiscOption.OhkoMoves.value in world.generated_misc.selected:
            for move in ["GUILLOTINE", "HORN_DRILL", "FISSURE"]:
                address = data.rom_addresses["AP_MoveData_Effect_" + move]
                write_bytes(patch, [0x65], address)  # false swipe effect
                address = data.rom_addresses["AP_MoveData_Power_" + move]
                write_bytes(patch, [0xFF], address)  # power 255
                address = data.rom_addresses["AP_MoveData_Accuracy_" + move]
                write_bytes(patch, [0xFF], address)  # accuracy 100%
                address = data.rom_addresses["AP_MoveData_PP_" + move]
                write_bytes(patch, [0x14], address)  # 20 PP

        if MiscOption.RadioTowerQuestions.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_N"] + 1
            # bad pokedex rating jingle
            write_bytes(patch, [0x9F], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y2"] + 1
            # increasing pokedex rating jingles
            write_bytes(patch, [0xA0], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y3"] + 1
            write_bytes(patch, [0xA1], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y4"] + 1
            write_bytes(patch, [0xA2], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y5"] + 1
            write_bytes(patch, [0xA3], address)
            for i in range(0, 5):
                answer = world.generated_misc.radio_tower_questions[i]
                # # 0x08 is iffalse (.WrongAnswer), 0x09 is iftrue (.WrongAnswer)
                byte = 0x08 if answer == "Y" else 0x09
                address = data.rom_addresses["AP_Misc_RadioTower_Q" + str(i + 1)]
                write_bytes(patch, [byte], address)

        if MiscOption.FanClubChairman.value in world.generated_misc.selected:
            # gives the chairman a 15/16 chance of repeating the rapidash rant each time
            address = data.rom_addresses["AP_Misc_Rapidash_Loop"] + 1
            write_bytes(patch, [1], address)

        if MiscOption.Amphy.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_Amphy"] + 1
            write_bytes(patch, [1], address)

        if MiscOption.SecretSwitch.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_SecretSwitch"] + 1
            write_bytes(patch, [1], address)

        if MiscOption.RedGyarados.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_RedGyarados"] + 1
            write_bytes(patch, [1], address)

        if MiscOption.RadioChannels.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_RadioChannels"]
            for channel_addr in world.generated_misc.radio_channel_addresses:
                write_bytes(patch, channel_addr.to_bytes(2, "little"), address + 1)
                address += 3

        if MiscOption.MomItems.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_MomItems"]
            for mom_item in world.generated_misc.mom_items:
                write_bytes(patch, [item_const_name_to_id(mom_item.item)], address + (8 * mom_item.index) + 7)

    if world.options.blind_trainers:
        address = data.rom_addresses["AP_Setting_Blind_Trainers"]
        write_bytes(patch, [0xC9], address)  # 0xC9 = ret

    if not world.options.item_receive_sound:
        address = data.rom_addresses["AP_Setting_ItemSFX"] + 1
        write_bytes(patch, [0], address)

    if world.options.reusable_tms:
        address = data.rom_addresses["AP_Setting_ReusableTMs"] + 1
        write_bytes(patch, [1], address)

    if world.options.guaranteed_catch:
        address = data.rom_addresses["AP_Setting_GuaranteedCatch"] + 1
        write_bytes(patch, [1], address)

    if world.options.minimum_catch_rate > 0:
        address = data.rom_addresses["AP_Setting_MinCatchrate"] + 1
        write_bytes(patch, [world.options.minimum_catch_rate], address)

    if world.options.randomize_music:
        for map_name, map_music in world.generated_music.maps.items():
            music_address = data.rom_addresses["AP_Music_" + map_name]
            # map music uses a single byte
            write_bytes(patch, [world.generated_music.consts[map_music].id], music_address)
        for i, music_name in enumerate(world.generated_music.encounters):
            music_address = data.rom_addresses["AP_EncounterMusic"] + i
            write_bytes(patch, [world.generated_music.consts[music_name].id], music_address)
        for script_name, script_music in world.generated_music.scripts.items():
            music_address = data.rom_addresses["AP_Music_" + script_name] + 1
            # script music is 2 bytes LE
            write_bytes(patch, world.generated_music.consts[script_music].id.to_bytes(2, "little"), music_address)

    if world.options.better_marts:
        mart_address = data.rom_addresses["Marts"]
        better_mart_address = data.rom_addresses["MartBetterMart"] - 0x10000
        better_mart_bytes = better_mart_address.to_bytes(2, "little")
        for i in range(33):
            # skip goldenrod and celadon
            if i not in [6, 7, 8, 9, 10, 11, 12, 24, 25, 26, 27, 28]:
                write_bytes(patch, better_mart_bytes, mart_address)
            mart_address += 2

    for hm in world.options.remove_badge_requirement.valid_keys:
        hm_address = data.rom_addresses["AP_Setting_HMBadges_" + hm] + 1
        requirement = [1] if hm in world.options.remove_badge_requirement else [
            world.options.hm_badge_requirements.value]
        write_bytes(patch, requirement, hm_address)

    exp_modifier_address = data.rom_addresses["AP_Setting_ExpModifier"] + 1
    write_bytes(patch, [world.options.experience_modifier], exp_modifier_address)

    elite_four_text = convert_to_ingame_text("{:02d}".format(world.options.elite_four_badges.value))
    write_bytes(patch, elite_four_text, data.rom_addresses["AP_Setting_VictoryRoadBadges_Text"] + 1)
    write_bytes(patch, [world.options.elite_four_badges - 1],
                data.rom_addresses["AP_Setting_VictoryRoadBadges"] + 1)
    write_bytes(patch, [world.options.radio_tower_badges - 1], data.rom_addresses["AP_Setting_RocketBadges"] + 1)

    mt_silver_text = convert_to_ingame_text("{:02d}".format(world.options.mt_silver_badges.value))
    write_bytes(patch, mt_silver_text, data.rom_addresses["AP_Setting_MtSilverBadges_Text"] + 1)
    write_bytes(patch, mt_silver_text, data.rom_addresses["AP_Setting_MtSilverBadges_Text2"] + 1)
    write_bytes(patch, [world.options.mt_silver_badges - 1], data.rom_addresses["AP_Setting_MtSilverBadges_Oak"] + 1)
    write_bytes(patch, [world.options.mt_silver_badges - 1], data.rom_addresses["AP_Setting_MtSilverBadges_Gate"] + 1)

    write_bytes(patch, [world.options.red_badges - 1], data.rom_addresses["AP_Setting_RedBadges"] + 1)

    if not world.options.johto_only:
        kanto_access_become_champion = [1] if (world.options.kanto_access_condition.value
                                               == KantoAccessCondition.option_become_champion) else [0]
        write_bytes(patch, kanto_access_become_champion, data.rom_addresses["AP_Setting_KantoAccess_Champion_1"] + 1)
        write_bytes(patch, kanto_access_become_champion, data.rom_addresses["AP_Setting_KantoAccess_Champion_2"] + 1)

        kanto_access_wake_snorlax = [1] if (world.options.kanto_access_condition.value
                                            == KantoAccessCondition.option_wake_snorlax) else [0]
        write_bytes(patch, kanto_access_wake_snorlax, data.rom_addresses["AP_Setting_KantoAccess_Snorlax_1"] + 1)
        write_bytes(patch, kanto_access_wake_snorlax, data.rom_addresses["AP_Setting_KantoAccess_Snorlax_2"] + 1)

        write_bytes(patch, [world.options.kanto_access_badges - 1],
                    data.rom_addresses["AP_Setting_KantoAccess_Badges"] + 1)
        kanto_badges_text = convert_to_ingame_text("{:02d}".format(world.options.kanto_access_badges.value))
        write_bytes(patch, kanto_badges_text, data.rom_addresses["AP_Setting_KantoAccess_Badges_Text"] + 1)

    if world.options.trainersanity:
        # prevents disabling gym trainers, among a few others
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_Trainersanity"] + 1)
        # removes events from certain trainers, to prevent disabling them.
        # the dw at +11 is the event flag.
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_BurglarDuncan"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_BurglarEddie"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM13"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM11"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM25"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntF3"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM24"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM14"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM15"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM3"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM4"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM5"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM6"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntF2"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM7"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM8"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM9"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_ScientistMarc"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM10"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_ExecutiveM2"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntF4"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_ScientistRich"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_ExecutiveF1"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM29"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM2"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntF1"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM16"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_ScientistJed"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM17"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM18"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_GruntM19"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_RocketMurkrow"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_SlowpokeGrunt"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_RaticateGrunt"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_ScientistRoss"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_ScientistMitch"] + 11)
        write_bytes(patch, [0xFF, 0xFF], data.rom_addresses["AP_Setting_Trainersanity_RocketBaseB3FRocket"] + 11)

    trainersanity_alerts_address = data.rom_addresses["AP_Setting_TrainersanityMessages"] + 1
    write_bytes(patch, [world.options.trainersanity_alerts], trainersanity_alerts_address)

    for i, script in enumerate(world.generated_phone_traps):
        address = data.rom_addresses["AP_Setting_PhoneCallTrapTexts"] + (i * 0x400)
        s_bytes = script.get_script_bytes()
        # write script text
        write_bytes(patch, s_bytes, address)
        # write script caller id
        address = data.rom_addresses["AP_Setting_SpecialCalls"] + (6 * i) + 2
        write_bytes(patch, [script.caller_id], address)

    phone_location_bytes = []
    for loc in world.generated_phone_indices:
        phone_location_bytes += list(loc.to_bytes(2, "little"))
    phone_location_address = data.rom_addresses["AP_Setting_Phone_Trap_Locations"]
    write_bytes(patch, phone_location_bytes, phone_location_address)

    start_inventory_address = data.rom_addresses["AP_Start_Inventory"]
    start_inventory = copy.deepcopy(world.options.start_inventory.value)
    start_inventory |= copy.deepcopy(world.options.start_inventory_from_pool.value)
    for item, quantity in start_inventory.items():
        if quantity == 0:
            quantity = 1
        while quantity:
            item_code = world.item_name_to_id[item]
            if item_code > 511:
                continue
            elif item_code > 255:
                item_code -= 256
            if quantity > 99:
                write_bytes(patch, [item_code, 99], start_inventory_address)
                quantity -= 99
            else:
                write_bytes(patch, [item_code, quantity], start_inventory_address)
                quantity = 0
            start_inventory_address += 2

    if world.options.free_fly_location.value in [FreeFlyLocation.option_free_fly,
                                                 FreeFlyLocation.option_free_fly_and_map_card]:
        free_fly_write = [0, 0, 0, 0]
        free_fly_write[int(world.free_fly_location.id / 8)] = 1 << (world.free_fly_location.id % 8)
        write_bytes(patch, free_fly_write, data.rom_addresses["AP_Setting_FreeFly"])

    if world.options.free_fly_location.value in [FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card]:
        map_fly_offset = int(world.map_card_fly_location.id / 8).to_bytes(2, "little")
        map_fly_byte = 1 << (world.map_card_fly_location.id % 8)
        write_bytes(patch, [map_fly_byte], data.rom_addresses["AP_Setting_MapCardFreeFly_Byte"] + 1)
        write_bytes(patch, map_fly_offset, data.rom_addresses["AP_Setting_MapCardFreeFly_Offset"] + 1)

    if world.options.remove_ilex_cut_tree:
        # Set cut tree tile to floor
        replace_map_tiles(patch, "IlexForest", 0, 11, [0x1])

    if world.options.skip_elite_four:
        # Lance's room is ID 7
        write_bytes(patch, [0x7], data.rom_addresses["AP_Setting_IndigoPlateauPokecenter1F_E4Warp"] + 4)

    route_32_open = [1] if world.options.route_32_condition.value == Route32Condition.option_none else [0]
    route_32_badge = [1] if world.options.route_32_condition.value == Route32Condition.option_any_badge else [0]
    route_32_egg = [1] if world.options.route_32_condition.value == Route32Condition.option_egg_from_aide else [0]

    write_bytes(patch, route_32_open, data.rom_addresses["AP_Setting_Route32Open"] + 1)
    write_bytes(patch, route_32_badge, data.rom_addresses["AP_Setting_Route32RequiresBadge"] + 1)
    write_bytes(patch, route_32_egg, data.rom_addresses["AP_Setting_Route32RequiresEgg"] + 1)

    if "North" in world.options.saffron_gatehouse_tea.value:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_SaffronRoute5Blocked"] + 1)
    if "East" in world.options.saffron_gatehouse_tea.value:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_SaffronRoute8Blocked"] + 1)
    if "South" in world.options.saffron_gatehouse_tea.value:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_SaffronRoute6Blocked"] + 1)
    if "West" in world.options.saffron_gatehouse_tea.value:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_SaffronRoute7Blocked"] + 1)

    if world.options.saffron_gatehouse_tea.value:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_TeaEnabled"] + 1)

    if world.options.east_west_underground.value:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_EastWestUndergroundEnabled"] + 1)

    if world.options.undergrounds_require_power.value in [UndergroundsRequirePower.option_neither,
                                                          UndergroundsRequirePower.option_east_west]:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_NorthSouthUndergroundOpen"] + 1)

    if (world.options.east_west_underground.value and
            world.options.undergrounds_require_power.value in [UndergroundsRequirePower.option_neither,
                                                               UndergroundsRequirePower.option_north_south]):
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_EastWestUndergroundOpen"] + 1)

    if world.options.remote_items:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_RemoteItems"])

    if world.options.require_itemfinder.value == RequireItemfinder.option_hard_required:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_ItemfinderRequired"] + 1)

    if world.options.goal.value != Goal.option_elite_four:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_SkipE4Credits"] + 1)

    if world.options.route_2_access.value == Route2Access.option_open:
        tiles = [0x01]  # ground
    elif world.options.route_2_access.value == Route2Access.option_ledge:
        tiles = [0x58, 0x0A]  # grass with left ledge, grass
    else:
        tiles = None

    if tiles:
        replace_map_tiles(patch, "Route2", 5, 1, tiles)

    if world.options.red_gyarados_access:
        whirlpool_tile = 0x07
        rock_tile = 0x0A
        water_tile = 0x35
        map_name = "LakeOfRage"
        replace_map_tiles(patch, map_name, 8, 10, [rock_tile, whirlpool_tile, 0x39])
        replace_map_tiles(patch, map_name, 7, 11, [0x30, water_tile, water_tile, rock_tile])
        replace_map_tiles(patch, map_name, 7, 12, [0x31, whirlpool_tile, 0x3A, 0x31])

    if world.options.blackthorn_dark_cave_access.value == BlackthornDarkCaveAccess.option_waterfall:
        map_name = "DarkCaveVioletEntrance"
        replace_map_tiles(patch, map_name, 6, 0, [0x11, 0x10])
        replace_map_tiles(patch, map_name, 6, 1, [0x08, 0x0A])
        replace_map_tiles(patch, map_name, 6, 2, [0x0C, 0x0E, 0x27, 0x0C, 0x0D, 0x0E])
        replace_map_tiles(patch, map_name, 6, 3, [0x2D, 0x2F, 0x2C, 0x2D, 0x2E, 0x2F])
        replace_map_tiles(patch, map_name, 9, 4, [0x04, 0x06])

        map_name = "DarkCaveBlackthornEntrance"
        replace_map_tiles(patch, map_name, 2, 7, [0x02])
        replace_map_tiles(patch, map_name, 2, 8, [0x02])

    if world.options.national_park_access.value == NationalParkAccess.option_bicycle:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_NationalParkBicycle"] + 1)

    if world.options.route_3_access == Route3Access.option_boulder_badge:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_PewterCityBadgeRequired"] + 1)

    # Set slot name
    for i, byte in enumerate(world.player_name.encode("utf-8")):
        write_bytes(patch, [byte], data.rom_addresses["AP_Seed_Name"] + i)

    patch.write_file("token_data.bin", patch.get_token_binary())

    out_file_name = world.multiworld.get_out_file_name_base(world.player)
    patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().pokemon_crystal_settings.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes
