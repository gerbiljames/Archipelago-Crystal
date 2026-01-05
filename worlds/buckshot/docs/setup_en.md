# Setup Guide for Buckshot Roulette Archipelago

## Requirements

- The latest Steam version of `Buckshot Roulette`
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)

## Installation

1.  Download `gml-7.0.1-custom.zip` from the latest release.

2.  Navigate to the directory on your PC containing you game installation.

    Using Steam:
    
    1. In Steam, right click `Buckshot Roulette` in the left sidebar.
    2. Click `Properties`.
    3. In the new window, click `Installed Files` in the left sidebar.
    4. Click `Browse...`. Your file manager should appear.
    5. Open `Buckshot Roulette_{os}` where `{os}` is your operating system.
    6. You should now see `BuckshotRoulette.exe`.

3.  Place the `/addons` folder from the Godot Mod Loader into this directory.

4.  Run the Buckshot Roulette executable with the following command line arguments:

    `--script addons/mod_loader/mod_loader_setup.gd`

    On Windows:

    1. Right-click `BuckshotRoulette.exe`, then click `Create shortcut`.

    2. Right-click the shortcut you created (typically named `BuckshotRoulette.exe - Shortcut`).
    then click `Properties`.

    3. In the `Shortcut` tab, add the above text to the end of the `Target` field.

    4. Run the shortcut.

5.  Wait for Godot Mod Loader to finish its installation. You will receive a prompt to restart
the game once this happens. You should now see two executables in your installation folder:
    - `BuckshotRoulette`
    - `BuckshotRoulette-vanilla`

    Launching the game from Steam will load the modded version by default.

6.  Create a `/mods` directory in your installation folder and place the Buckshot Roulette Archipelago mod (`asdfwyay-APBuckshot-{version}.zip`) in there.

7.  Launch Buckshot Roulette and enjoy! A notification will appear on your first launch stating
that new mods have been installed. When reaching the start menu, the `MULTIPLAYER` button
should be replaced with an `ARCHIPELAGO` button.

## Updating

1.  Navigate to the `/mods` directory in your Buckshot Roulette installation folder.

2.  Replace the old mod ZIP with the new one (`asdfwyay-APBuckshot-{version}.zip`).

3.  Launch Buckshot Roulette and enjoy! A notification will appear upon launching stating
that new mods have been installed.

## Connecting to a Game

1.   From the main menu, click `ARCHIPELAGO`. A menu should appear in the top left.
2.   Enter your slot name, server address, port, and password if needed.
3.   Click `CONNECT`.
4.   Wait until the status label in the menu updates to `CONNECTED`.
5.   Close the menu by clicking `CLOSE`.
6.   When ready, start playing by clicking `START`.