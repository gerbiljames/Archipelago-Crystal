# Troubleshooting

## Setup

### The name `...\Buckshot Roulette.exe"--script'` specified in the Target box is not valid.
Add a space between `Buckshot Roulette.exe` and `--script`.

## Connecting

### The client displays either the "Invalid Slot" or "Invalid Password" error message when attempting to connect even though the credentials match.
Lowercase letters in the font used for the input fields look like uppercase letters, yet the input fields are case-sensitive. Therefore, it's likely that you input at least one lowercase letter in your slot name or password when it was meant to be uppercase.

Re-input your credentials, ensuring that the `Slot` and `Password` fields match exactly.

### The client hangs on `Connecting...` and no error message is received.
Ensure the server address and port are correct.

If the Archipelago room is very large and your mod version is less than `0.1.1-hotfix.1`, update the mod and try again.

## Playing

### Picking up the shotgun softlocks the game (without freezing or crashing)
You likely installed the default Godot Mod Loader instead of the custom one.
1. Delete the modded executable and rename `Buckshot Roulette-vanilla` to `Buckshot Roulette`.

2. Reinstall the mod using the [custom mod loader](https://github.com/asdfwyay/APBuckshot-Client/releases/tag/gml-7.0.1-custom).

