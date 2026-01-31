import math
import hashlib
import itertools
import os
import pkgutil
import struct
import unicodedata

from typing import TYPE_CHECKING
import settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension

from . import Items
from .Locations import ID_BASE
from .Options import CourseOrder, ShuffleDriftAbilities, ConsistentItemBoxes

if TYPE_CHECKING:
    from . import MK64World


# ROM ADDRESSES
class Addr:
    # *** ROM ADDRESSES ***
    # ** Native **
    COURSE_IDS = 0xF37B4
    COURSE_NAMEPLATES = 0x12F772
    RESULTS_MUSIC_REPETITIONS = 0xBDA883
    # ** Basepatch **
    SAVE = 0xC00000
    SAVE_SIZE = 0x200
    SAVE_LOCKED_ITEM_CLUSTERS = SAVE + 0x1B
    SAVE_LOCKED_ITEM_CLUSTERS_SIZE = 9
    SAVE_UNCHECKED_LOCATIONS = SAVE_LOCKED_ITEM_CLUSTERS + SAVE_LOCKED_ITEM_CLUSTERS_SIZE
    SAVE_UNCHECKED_LOCATIONS_SIZE = 56
    SAVE_IDENTIFIED_ITEM_BOXES = SAVE_UNCHECKED_LOCATIONS + SAVE_UNCHECKED_LOCATIONS_SIZE
    SAVE_IDENTIFIED_ITEM_BOXES_SIZE = 43
    PLAYER_NAME = SAVE + SAVE_SIZE
    PLAYER_NAME_SIZE = 64
    SEED_NAME = PLAYER_NAME + PLAYER_NAME_SIZE
    SEED_NAME_SIZE = 20
    GENERATION_DONE = SEED_NAME + SEED_NAME_SIZE
    GENERATION_LOCKED = GENERATION_DONE + 1
    # Game Settings
    TWO_PLAYER_POWERS = GENERATION_LOCKED + 1
    GAME_MODE = TWO_PLAYER_POWERS + 1
    MIRROR_COURSES = GAME_MODE + 1
    TWO_LAP_COURSES = MIRROR_COURSES + 2
    FREE_MINI_TURBO = TWO_LAP_COURSES + 2
    SHUFFLE_RAILINGS = FREE_MINI_TURBO + 1
    FEATHER_AVAILABLE = SHUFFLE_RAILINGS + 1
    CONSISTENT_ITEM_BOXES = FEATHER_AVAILABLE + 1
    ENGINE_CLASSES = CONSISTENT_ITEM_BOXES + 1
    # Generation Flags
    # AP Items and pickup strings
    ITEMS = 0xC002C8  # APItem[583] at 3 bytes each
    ITEM_SIZE = 3
    PICKUP_PLAYER_NAMES = 0xC009A0  # char[220][16]
    ASCII_PLAYER_NAME_SIZE = 16
    PICKUP_ITEM_NAMES = 0xC01760  # char[220][40]
    ITEM_NAME_SIZE = 40

    # *** RAM ADDRESSES ***
    GAME_STATUS_BYTE = 0x400019
    NUM_ITEMS_RECEIVED = 0x40001A
    LOCATIONS_UNCHECKED = 0x400024
    ENGINE_CLASSES_RAM = 0x400260
    RECEIVE_ITEM_ID = 0x40028E
    RECEIVE_CLASSIFICATION = RECEIVE_ITEM_ID + 1
    RECEIVE_PLAYER_NAME = RECEIVE_CLASSIFICATION + 1
    RECEIVE_ITEM_NAME = RECEIVE_PLAYER_NAME + ASCII_PLAYER_NAME_SIZE


class MK64APPatchExtension(APPatchExtension):
    game = "Mario Kart 64"

    @staticmethod
    def apply_crc(_: APProcedurePatch, rom: bytes) -> bytes:
        # Adapted from espeon65536's version in oot/data/crc.py

        rom_data = bytearray(rom)

        t1 = t2 = t3 = t4 = t5 = t6 = 0xF8CA4DDC
        u32 = 0xFFFFFFFF

        m1 = rom_data[0x1000:0x1000 + 0x100000]
        words = struct.unpack(f'>{len(m1) // 4}I', m1)

        m2 = rom_data[0x750:0x750 + 0x100]
        words2 = struct.unpack(f'>{len(m2) // 4}I', m2)

        for d, d2 in zip(words, itertools.cycle(words2)):
            # keep t2 and t6 in u32 for comparisons; others can wait to be truncated
            if ((t6 + d) & u32) < t6:
                t4 += 1

            t6 = (t6 + d) & u32
            t3 ^= d
            shift = d & 0x1F
            r = ((d << shift) | (d >> (32 - shift)))
            t5 += r

            if t2 > d:
                t2 ^= r & u32
            else:
                t2 ^= t6 ^ d

            t1 += t5 ^ d

        crc0 = (t6 ^ t4 ^ t3) & u32
        crc1 = (t5 ^ t2 ^ t1) & u32

        crc = struct.pack('>II', crc0, crc1)

        rom_data[0x10:0x10 + len(crc)] = bytearray(crc)

        return bytes(rom_data)


class MK64ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Mario Kart 64"
    hash = "3a67d9986f54eb282924fca4cd5f6dff"
    patch_file_ending = ".apmk64"
    result_file_ending = ".z64"

    procedure = [
        ("apply_bsdiff4", ["basepatch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
        ("apply_crc", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(settings.get_settings().mk64_options.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes


def write_tokens(world: "MK64World", patch: MK64ProcedurePatch, output_directory: str) -> None:

    multiworld = world.multiworld
    player = world.player
    opt = world.opt
    random = world.random

    # PATCHING START

    # Patch save file
    save_id = hashlib.md5((multiworld.seed_name + multiworld.player_name[player]).encode()).digest()[:8]
    locked_courses = 0xFFFF << 16 - opt.locked_courses & 0xFFFF
    drift = ((opt.drift == ShuffleDriftAbilities.option_off and 0xAAAA) or
             (opt.drift == ShuffleDriftAbilities.option_free_drift and 0x5555) or 0)
    blues = 0b11 if opt.special_boxes else 0
    kart_unlocks = sum(1 << Items.item_name_groups["Karts"].index(kart) for kart in world.starting_karts)
    tires_off_road = 0 if opt.traction else 0xFF
    tires_winter = 0 if opt.traction else 0xFF
    locked_cups = 0b1110  # only Mushroom Cup starts unlocked
    switches = 0 if opt.fences else 0b1111
    misc_byte = 1 if opt.box_respawning else 0b101  # game_clear (initially 0), connected status bit (always 1)

    # Pack to bytes ordered to the basepatch's SaveData struct bitfields
    write_bytes(patch, Addr.SAVE, save_id)  # replaces DATETIME pseudo-hash in basepatch
    write_int16(patch, Addr.SAVE + 0x8, locked_courses)
    write_int16(patch, Addr.SAVE + 0xA, drift)
    write_byte(patch, Addr.SAVE + 0xF, blues)
    write_byte(patch, Addr.SAVE + 0x14, kart_unlocks)
    write_byte(patch, Addr.SAVE + 0x15, tires_off_road)
    write_byte(patch, Addr.SAVE + 0x16, tires_winter)
    write_byte(patch, Addr.SAVE + 0x17, (locked_cups << 4) | switches)
    write_byte(patch, Addr.SAVE + 0x19, misc_byte)

    # Patch Locked Item Clusters
    initial_locked_clusters = bytearray(Addr.SAVE_LOCKED_ITEM_CLUSTERS_SIZE)
    for c, cluster in enumerate(world.shuffle_clusters):
        if cluster:
            initial_locked_clusters[c // 8] |= 1 << c % 8
    write_bytes(patch, Addr.SAVE_LOCKED_ITEM_CLUSTERS, initial_locked_clusters)

    # Patch player name and multiworld seed_name for later ROM authentication with the client
    player_name_bytes = multiworld.player_name[player].encode("utf-8")
    if len(player_name_bytes) > 64:
        raise ValueError(f"Player name {multiworld.player_name[player]} was longer than the 64 byte expectation.")
    write_bytes(patch, Addr.PLAYER_NAME, [0] * Addr.PLAYER_NAME_SIZE)
    write_bytes(patch, Addr.PLAYER_NAME, player_name_bytes)
    seed_name_bytes = multiworld.seed_name.encode("utf-8")
    if len(seed_name_bytes) > 20:
        raise ValueError(f"Multiworld.seed_name {multiworld.seed_name} was longer than the 20 byte expectation.")
    write_bytes(patch, Addr.SEED_NAME, [0] * Addr.SEED_NAME_SIZE)
    write_bytes(patch, Addr.SEED_NAME, seed_name_bytes)

    # Patch game settings
    mirror_courses = 0
    for i in range(16):
        if random.random() < opt.mirror_chance:
            mirror_courses |= 1 << i
    two_lap_mapping = {0: 0, 1: 0x8000, 2: 0x0100, 3: 0x8100}
    two_lap_courses = two_lap_mapping[opt.two_lap_courses]
    write_byte(patch, Addr.TWO_PLAYER_POWERS, opt.two_player)
    write_byte(patch, Addr.GAME_MODE, opt.mode)
    write_byte(patch, Addr.FREE_MINI_TURBO, opt.drift == ShuffleDriftAbilities.option_free_mini_turbo)
    write_int16(patch, Addr.MIRROR_COURSES, mirror_courses)
    write_int16(patch, Addr.TWO_LAP_COURSES, two_lap_courses)
    write_byte(patch, Addr.SHUFFLE_RAILINGS, opt.railings)
    write_byte(patch, Addr.FEATHER_AVAILABLE, opt.feather)
    write_byte(patch, Addr.CONSISTENT_ITEM_BOXES, opt.consistent)
    if opt.consistent == ConsistentItemBoxes.option_on:
        write_bytes(patch, Addr.SAVE_IDENTIFIED_ITEM_BOXES, [0xFF] * Addr.SAVE_IDENTIFIED_ITEM_BOXES_SIZE)
    write_int16(patch, Addr.ENGINE_CLASSES, opt.low_engine)
    write_int16(patch, Addr.ENGINE_CLASSES + 2, opt.middle_engine)
    write_int16(patch, Addr.ENGINE_CLASSES + 4, opt.high_engine)
    write_byte(patch, Addr.GENERATION_DONE, 1)
    write_byte(patch, Addr.GENERATION_LOCKED, 1)

    # Write custom course order
    if opt.course_order != CourseOrder.option_vanilla:
        course_ids = [0x8, 0x9, 0x6, 0xB,
                      0xA, 0x5, 0x1, 0x0,
                      0xE, 0xC, 0x7, 0x2,
                      0x12, 0x4, 0x3, 0xD]
        course_nameplate_ids = [0x4C, 0x50, 0x43, 0x59,
                                0x54, 0x3E, 0x2A, 0x25,
                                0x65, 0x5D, 0x48, 0x2F,
                                0x75, 0x3A, 0x34, 0x61]
        for i, c in enumerate(world.course_order):
            write_byte(patch, Addr.COURSE_IDS + 2 * i + 1, course_ids[c])
            write_byte(patch, Addr.COURSE_NAMEPLATES + 20 * math.floor(1.25 * i), course_nameplate_ids[c])

    # Patch optional fixes
    # The basepatch may already have the music fix set, so we set either case here just in case
    write_byte(patch, Addr.RESULTS_MUSIC_REPETITIONS, 0x2 if opt.fix_music else 0x40)

    # Write items, and marked unavailable locations as checked
    initial_unchecked_locs = bytearray(Addr.SAVE_UNCHECKED_LOCATIONS_SIZE)
    for i, loc in enumerate(multiworld.get_locations(player)):
        if loc.address is None:  # Skip Victory Event Location
            continue
        local_loc_id = loc.address - ID_BASE
        initial_unchecked_locs[local_loc_id // 8] |= 1 << local_loc_id % 8
        # Write items
        addr = Addr.ITEMS + Addr.ITEM_SIZE * local_loc_id
        write_byte(patch, addr + 1, loc.item.classification & 0b111)  # 0=FILLER,1=PROGRESSION,2=USEFUL,4=TRAP
        write_byte(patch, addr + 2, i)  # pickup_id, used by the game to reference player name and item name
        pickup_item_name = unicodedata.normalize("NFKD", loc.item.name) \
            .encode("ascii", "ignore")[:Addr.ITEM_NAME_SIZE]
        write_bytes(patch, Addr.PICKUP_ITEM_NAMES + i * Addr.ITEM_NAME_SIZE, pickup_item_name)
        if loc.item.player == player:
            write_byte(patch, addr, loc.item.code - ID_BASE)  # local_id (0 to 211)
        else:
            write_byte(patch, addr, 0xFF)  # local_id of 0xFF indicates nonlocal item
            pickup_player_name = unicodedata.normalize("NFKD", multiworld.player_name[loc.item.player]) \
                .encode("ascii", "ignore")[:Addr.ASCII_PLAYER_NAME_SIZE]
            write_bytes(patch, Addr.PICKUP_PLAYER_NAMES + Addr.ASCII_PLAYER_NAME_SIZE * i, pickup_player_name)
    write_bytes(patch, Addr.SAVE_UNCHECKED_LOCATIONS, initial_unchecked_locs)

    patch.write_file("basepatch.bsdiff4", pkgutil.get_data(__name__, "data/mk64-ap-basepatch.bsdiff"))
    patch.write_file("token_data.bin", patch.get_token_binary())

    out_file_name = world.multiworld.get_out_file_name_base(world.player)
    patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))


def write_byte(patch: MK64ProcedurePatch, address: int, value: int):
    patch.write_token(APTokenTypes.WRITE, address, value.to_bytes(1, byteorder="big"))


def write_bytes(patch: MK64ProcedurePatch, startaddress: int, values: list[int] | bytes | bytearray):
    if type(values) == bytearray or type(values) == list:
        patch.write_token(APTokenTypes.WRITE, startaddress, bytes(values))
    else:
        patch.write_token(APTokenTypes.WRITE, startaddress, values)


def write_int16(patch: MK64ProcedurePatch, address: int, value: int):
    value = value & 0xFFFF
    patch.write_token(APTokenTypes.WRITE, address, value.to_bytes(2, byteorder="big"))
