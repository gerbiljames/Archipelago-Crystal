from dataclasses import replace
from math import floor
from typing import TYPE_CHECKING

from . import MiscOption

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def randomize_mischief(world: "PokemonCrystalWorld"):
    if not world.options.enable_mischief: return

    # Decide which mischief is active
    all_mischief = world.generated_misc.selected

    lower_count = len(all_mischief) // 2
    upper_count = floor(len(all_mischief) * 0.75)
    mischief_count = world.random.randint(lower_count, upper_count)

    world.generated_misc = replace(world.generated_misc, selected=world.random.sample(all_mischief, mischief_count))

    if MiscOption.RadioTowerQuestions.value in world.generated_misc.selected:
        # Randomize Yes/No answers for Radio Card quiz
        world.generated_misc = replace(
            world.generated_misc,
            radio_tower_questions=[world.random.choice(("Y", "N")) for _ in
                                   world.generated_misc.radio_tower_questions]
        )

    if MiscOption.FuchsiaGym.value in world.generated_misc.selected:
        # shuffle positions of trainers in fuchsia gym
        fuchsia_gym_trainers = list(world.generated_misc.fuchsia_gym_trainers)
        world.random.shuffle(fuchsia_gym_trainers)
        world.generated_misc = replace(world.generated_misc, fuchsia_gym_trainers=fuchsia_gym_trainers)

    if MiscOption.SaffronGym.value in world.generated_misc.selected:
        shuffled_saffron_warps = {}
        for direction in ("NW", "N", "NE", "W", "E", "SW", "SE"):
            numbers = [1, 2, 3, 4]
            world.random.shuffle(numbers)
            shuffled_saffron_warps[direction] = numbers

        new_pairs = []
        for pair in world.generated_misc.saffron_gym_warps.pairs:
            new_pair = []
            for i in range(0, 2):
                if pair[i] in ("START", "END"):
                    new_pair.append(pair[i])
                    continue
                direction = pair[i].split("_")[0]
                number = int(pair[i].split("_")[1])
                new_number = shuffled_saffron_warps[direction][number - 1]
                new_pair.append(f"{direction}_{new_number}")
            new_pairs.append(new_pair)
        world.generated_misc = replace(world.generated_misc,
                                       saffron_gym_warps=replace(world.generated_misc.saffron_gym_warps,
                                                                 pairs=new_pairs))

    if MiscOption.RadioChannels.value in world.generated_misc.selected:
        new_addresses = list(world.generated_misc.radio_channel_addresses)
        world.random.shuffle(new_addresses)
        world.generated_misc = replace(world.generated_misc, radio_channel_addresses=new_addresses)

    if MiscOption.MomItems.value in world.generated_misc.selected:
        good_items = ["MASTER_BALL", "NUGGET", "PP_UP", "RARE_CANDY", "SACRED_ASH", "LUCKY_EGG"]
        world.generated_misc = replace(world.generated_misc,
                                       mom_items=[replace(item, item=world.random.choice(good_items)) for item in
                                                  world.generated_misc.mom_items])


def get_misc_spoiler_log(world: "PokemonCrystalWorld", write):
    write(f"{len(world.generated_misc.selected)} mischief options enabled.\n")

    if MiscOption.RadioTowerQuestions.value in world.generated_misc.selected:
        radio_tower_answers = " -> ".join(
            ["YES" if answer == "Y" else "NO" for answer in world.generated_misc.radio_tower_questions])
        write(f"\nRadio Tower Quiz Answers:\n{radio_tower_answers}\n")

    if MiscOption.SaffronGym.value in world.generated_misc.selected:
        saffron_map = []
        # draw the walls in saffron gym
        for y in range(0, 17):
            saffron_map.append(["█" if x in (7, 15) or y in (5, 11) else " " for x in range(0, 23)])

        character = ord("A")  # we will increment this while drawing the warps
        for pair in world.generated_misc.saffron_gym_warps.pairs:
            for warp in pair:
                x, y = world.generated_misc.saffron_gym_warps.warps[warp].coords
                # cosmetic fudging
                x = x + 2 if x > 10 else x
                y = y - 2 if warp != "END" else y
                saffron_map[y][x] = chr(character)  # add warp letter
            character += 1  # next letter
        saffron_map[7][9] = "X"  # sabrina
        saffron_map[16][10] = "░"  #
        saffron_map[16][11] = "░"  # entrance
        saffron_map[16][12] = "░"  #

        write("\nSaffron Gym Warps:\n")
        write("\n".join(["".join(line) for line in saffron_map]))

    if MiscOption.FuchsiaGym.value in world.generated_misc.selected:
        # sum of x + y for each position
        fuchsia_positions = {
            11: "South-West",
            12: "Center",
            16: "South",
            13: "North-East",
            6: "North"
        }
        # janine is the first trainer in the list
        position = sum(world.generated_misc.fuchsia_gym_trainers[0])
        if fuchsia_positions[position]:
            write(f"\nFuchsia Gym Janine Position: {fuchsia_positions[position]}")
