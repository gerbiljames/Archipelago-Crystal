# Pokémon Crystal Archipelago

## What does randomization do to this game?

Some changes have been made to the base game for this randomizer:

- The director is always in the underground warehouse, even when Radio Tower isn't occupied
- The card key door in Goldenrod Department Store B1F unlocks with the Card Key in your Pack
- Time based checks such as the Day of the Week siblings and the Celadon Mansion roof guy are always available
    - The hidden items under Freida and Wesley have been moved a tile across to remain accessible
- The Ship between Olivine and Vermilion is always present in non-Johto-Only-games, even before entering Hall of Fame,
  and available to ride with the S.S. Ticket
- Misty is always in Cerulean Gym
- A ledge on Route 45 has been moved so all items and trainers can be accessed in 2 passthroughs
- For options which enable it, the Kanto badges map to the following HMs:
    - HM01 Cut - Cascade Badge
    - HM02 Fly - Thunder Badge
    - HM03 Surf - Soul Badge
    - HM04 Strength - Rainbow Badge
    - HM05 Flash - Boulder Badge
    - HM06 Whirlpool - Volcano Badge
    - HM07 Waterfall - Earth Badge
- TM02 and TM08 will always be Headbutt and Rock Smash respectively, and are always reusable
- Trade evolutions have been changed to make them possible in a solo run of the game:
    - Regular trade evolutions now evolve at level 37
    - Held item trade evolutions evolve when their evolution item is used on them, as you would an evolution stone
- Eevee evolves into Espeon and Umbreon with the Sun Stone and Moon Stone respectively
- Happiness evolutions are logically tied to access to the Goldenrod Underground or Pallet Town. The younger haircut
  brother and Daisy will max out a Pokémon's happiness and are always available
- Unown will only appear in the wild after solving one puzzle in the Ruins of Alph. Prior to that, any encounter that
  would have been Unown will instead play its cry
- Tin Tower 1F is accessible once you obtain the Clear Bell.
- Tin Tower 2F+ is accessible once the aforementioned condition is met, and you have the Rainbow Wing. Both are items in
  the multiworld
- Eusine will give you an Eon Mail if you talk to him in Tin Tower 1F after seeing Suicune in the overworld at all
  possible locations, which you can visit in any order
- The Celebi Event can be activated by giving the multiworld item GS Ball to Kurt after clearing Slowpoke Well and
  defeating the rival in Azalea
- The event which usually grants the GS Ball in Goldenrod Pokécenter 1F activates after becoming champion
- The man who gives a reward for having all badges in Vermilion City only checks for the 8 Kanto badges
- The Ruins of Alph Ho-Oh item chamber is accessible by owning the Rainbow Wing
- A shop has been added to 2F of all Pokémon Centers, you can customise what this shop sells using the `build_a_mart`
  option, the shop will always sell Poké Balls and Escape Ropes
- An NPC which allows you to fight a random wild Pokémon has been added to 2F of all Pokémon Centers, this fight awards
  money and exp, but does not grant Pokédex entries and is not catchable
- If it is randomized, Professor Elm will tell you your goal by talking to him at his lab or calling him

## What items and locations get randomized?

By default, items from item balls and items given by NPCs are randomized.
Badges can be either vanilla, shuffled or randomized. Pokégear and its card modules can be vanilla or randomized.
If Johto Only mode is enabled, items in Kanto will not be randomized and Kanto will be inaccessible.
The S.S. Ticket given by Elm after beating the Elite 4 will also be replaced by the Silver Wing.

There are options to include more items in the pool:

- Randomize Hidden Items: Adds hidden items to the pool
- Randomize Berry Trees: Adds berry tree items to the pool
- Trainersanity: Adds a reward for beating trainers to the pool
- Dexsanity: A Pokémon's Dex entry can hold a check. This is tied to specific Pokémon
- Dexcountsanity: A certain amount of Dex entries hold checks. This is not tied to specific Pokémon but a total
- Shopsanity: Includes shop items in the pool
- Grasssanity: Cutting every grass tile is a location
- Bug Catching Contest: Shuffles prizes for the bug catching contest, from participating to winning
- Randomize Pokémon Requests: Adds Bill's Grandpa's rewards and the Lake of Rage Magikarp prize to the pool
- Randomize Phone Calls: Adds items from trainer phone calls to the pool

## What other changes are made to the game?

Many additional quality of life changes have been implemented:

- A new text speed option, Instant, is added to the options menu in game.
- The A and/or B buttons can be used as turbo buttons to speed through dialogues
- When battle scenes are turned off, HP reduction and XP gain animations are skipped
- The Battle Scene option is more granular, with the fastest choice, Speedy, cutting nearly every animation
- You can hold B to run. An Auto-run option also exists, and if enabled, B prevents you from running
- Many other options were added to drastically speed up gameplay, including: Rods can always work, Uncaught Pokémon can
  be more likely to appear, Trainers can be blind, etc.
- Lag in menus has been removed
- The Bicycle can be used indoors
- The Escape Rope can be used in more interiors, such as Gyms
- If a repel runs out and you have more in your Pack, you will be prompted to use another
- Pokémon growth rates are always normalized (Medium-Fast for non-Legendary Pokémon, Slow for Legendary Pokémon)
- The clock reset password system has been removed, you can reset the clock with Down + Select + B on the title screen
- An in-game option for not requiring Field Moves to be taught was added. To keep Fly, Flash, and other Field Moves
  accessible, an additional menu is made available by pressing Select on the Start Menu
- You can respawn all static events by talking to the Time Capsule person in the second floor of any PokéCenter
- You can teleport back to your starting town by selecting "Go Home" in the start menu

## What does another world's item look like in Pokémon Crystal?

Items from other worlds will print the item name and the name of the receiving player when collected. Due to
limitations with the game's text, these names are truncated at 16 characters, and special characters not found in the
font are replaced with question marks.

## When the player receives an item, what happens?

A sound effect will play when an item is received if the Item Receive Sound option is enabled. Different sounds will
play to distinguish progression items and traps.

## Can I play offline?

Yes, the game does not need to be connected to the client for solo seeds. Connection is only required for sending and
receiving items. This does not apply when `remote_items` is enabled.

---

# Pokémon Crystal Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- An English (UE) Pokémon Crystal v1.0 or v1.1 ROM. The Archipelago community cannot provide this.
    - A valid v1.1 ROM can be extracted from the 3DS eShop release of the game.
- One of the following:
    - [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 or later. 2.11.1 is recommended.
    - [mGBA](https://mgba.io) 0.10.3 or later.
        - You will also need
          the [mGBA to Bizhawk Client connector script](https://gist.github.com/Zunawe/d41677500b08694c9985f67f41896cc5).
          You should add it to `data/lua/` in your Archipelago install.

### Configuring BizHawk

Once you have installed BizHawk, open `EmuHawk.exe` and change the following settings:

- On BizHawk 2.8 or earlier, navigate to `Config -> Customize` and click on the Advanced tab. Change the Lua core
  from `NLua+KopiLua` to `Lua+LuaInterface`, then restart EmuHawk. This step is not required on BizHawk 2.9 or later.
- Under `Config -> Customize -> Advanced`, make sure the box for AutoSaveRAM is checked, and click the 5s button.
  This reduces the possibility of losing save data in emulator crashes.
- In `Config -> Customize`, enable `Run in background`. This will prevent the game from losing connection to the client
  when tabbed out.
- To adjust controller settings, open a Game Boy or Game Boy Color game (`.gb` or `.gbc`) and then navigate to
  `Config -> Controllers...`. This menu may not be available if a game is not already open.
- Ensure that `Config -> Preferred Cores -> GB in SGB` is disabled.

### Configuring mGBA

Once you have installed mGBA, open `mGBA`, navigate to Settings/Preferences, and change the following setting:

- In `Game Boy`, under Models, select `Game Boy Color (CGB)` for all models.

## Optional Software

[Pokémon Crystal AP Tracker](https://github.com/palex00/crystal-ap-tracker/releases/latest) for use
with [PopTracker](https://github.com/black-sliver/PopTracker/releases/latest)

## Generating and Patching a Game

1. Add `pokemon_crystal.apworld` to your `custom_worlds` folder in your Archipelago install. It should not be in
   `lib\worlds`.
2. Create your options file (YAML). You can make one by choosing Generate Templates
   from the Archipelago Launcher. From there, you can edit the `.yaml` in any text editor.
3. Follow the general Archipelago instructions
   for [generating a game on your local installation](https://archipelago.gg/tutorial/Archipelago/setup/en#on-your-local-installation).
   This will generate an output file for you. Your patch file will have the `.apcrystal` file extension and will be
   inside the output file.
4. Open `ArchipelagoLauncher.exe`.
5. Select "Open Patch" on the left side and select your patch file.
6. If this is your first time patching, you will be prompted to locate your vanilla ROM.
7. A patched `.gbc` file will be created in the same place as the patch file.
8. On your first time opening a patch with BizHawk Client, you will also be asked to locate `EmuHawk.exe` in your
   BizHawk install. For mGBA users, you can select `Cancel` and manually open mGBA.

### Option Overrides

Pokemon Crystal has several options which do not affect Archipelago's logic, and as such can be changed after
generation without significantly changing the randomizer experience.

To do that, open the `host.yaml` file in your Archipelago folder and locate the `pokemon_crystal_settings` section.
In it, add an `option_overrides` setting like so:

```yaml
pokemon_crystal_settings:
  rom_file: "Pokemon - Crystal Version (UE) [C][!].gbc"
  option_overrides:
    # Enter your overrides here
```

You can then type in the options you would like to override as you would in a player YAML. Option weights and triggers
are supported.

The following options can always be overridden: `trainer_name`, `trainer_gender`, `trainer_palette`, `rival_name`,
`start_time`, `game_options`, `field_move_menu_order`, `default_pokedex_mode`, `shopsanity_restrict_rare_candies`,
`reusable_tms`, `minimum_catch_rate`, `skip_elite_four`, `better_marts`, `build_a_mart`, `experience_modifier`,
`starting_money`.

You can change these settings at any time after patching the ROM and re-apply them by patching the ROM again. Your
save data will be preserved.

If you're playing a single-player seed, and you don't care about autotracking or hints, you can stop here, close the
client, and load the patched ROM in any emulator. However, for multiworlds and other Archipelago features, continue
below using BizHawk or mGBA as your emulator.

## Connecting to a Server

By default, opening a patch file will do steps 1-5 below for you automatically. Even so, keep them in your memory just
in case you have to close and reopen a window mid-game for some reason.

1. Pokémon Crystal uses Archipelago's BizHawk Client. If the client isn't still open from when you patched your game,
   you can re-open it from the launcher.
2. Ensure EmuHawk or mGBA is running the patched ROM.
3. In EmuHawk:
    - Go to `Tools > Lua Console`. This window must stay open while playing.
    - In the Lua Console window, go to `Script > Open Script...`.
    - Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.
4. In mGBA:
    - Go to `Tools > Scripting...`. This window must stay open while playing.
    - Go to `File > Load Script...`.
    - Navigate to your Archipelago install folder and open `data/lua/connector_bizhawkclient_mgba.lua`.
5. The emulator and client will eventually connect to each other. The BizHawk Client window should indicate that it
   connected and recognized Pokémon Crystal.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect. It is
perfectly safe to make progress offline; everything will re-sync when you reconnect.

## Auto-Tracking

Pokémon Crystal has a fully functional map tracker that supports auto-tracking.

1. Download [Pokémon Crystal AP Tracker](https://github.com/palex00/crystal-ap-tracker/releases/latest) and
   [PopTracker](https://github.com/black-sliver/PopTracker/releases/latest).
2. Put the tracker pack into `packs/` in your PopTracker install.
3. Open PopTracker, and load the Pokémon Crystal pack.
4. For autotracking, click on the "AP" symbol at the top.
5. Enter the Archipelago server address (the one you connected your client to), slot name, and password. If you did not
   set a password for your room, leave that field empty.
