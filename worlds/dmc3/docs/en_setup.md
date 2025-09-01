# Devil May Cry 3 (HD Collection)

## Requirements
DMC HD Collection on Steam

GOG Version is untested and most likely will not work (Please do reach out if you have it on GOG though, I would be happy to add support)


Pirated/Cracked copies are not supported, buy the game.
## 0. Backup Save File
While the randomizer does use its own save folder separate from Steam's. It is still recommended that you make a backup of your save file.
The file can be found at

```C:\Program Files (x86)\Steam\userdata\85588318\631510\remote\dmc3.sav```

Or a similar location, depending on where Steam is installed
## 1. Downgrade your game
Follow the instructions from the link below to downgrade your game to the version compatible with the mod.

https://github.com/serpentiem/ddmk?tab=readme-ov-file#devil-may-cry-hd-collection

If you have used DDMK or DMC3-Crimson before, chances are your game is already properly downgraded. 

Note: The randomizer currently does not verify whether you are on the correct version or not. But chances are if it crashes upon trying to boot or connect to a room. Then the game has not been properly downgraded.
## 2. Install the randomizer.
If you already have a `dinput8.dll` from another mod, rename it to something else and extract the randomizers `dinput8.dll` into the same directory as `dmc3.exe` 

The randomizer will load up DDMK or Crimson if it is installed. 

Note: If you have another mod that uses `dinput8.dll` to load up, please let me know and I can try to make it so the rando will load it as well upon start.

If the mod has been successfully installed, start up DMC3 and you should have a console window as well as a GUI window or a modified DDMK overlay. 

## 3. Connect to a room
To connect to a room, open up the UI for the mod. This is either a separate window outside the game. Or if you have DDMK installed, it is your DDMK menu.

Fill in the URL, Username and Password and then connect.

If for some reason the mod doesn't seem to be connecting despite correct information, try restarting the game.

Once you are connected, you must go to load and select the save file in the first slot. Do not start a new game.

Then you may start at Mission #1 at any difficulty.
## 4. Optional: Start up DMC3 straight from the exe file

For those who are also annoyed by the launcher's slowness and would prefer to have a shortcut that directly launches DMC3. There is a `steam_appid.txt` file in the zip, put this in the same place as your `dmc3.exe` and then just launch the exe

This also works for the same for DMC1 and 2, DMC2 however will default to Dante unless launched with `lucia` as an argument.

I.e A shortcut to DMC2 that is setup with this as the `Target`

```"C:\Program Files (x86)\Steam\steamapps\common\Devil May Cry HD Collection\dmc2.exe" lucia```

## Uninstallation

To disable/remove the mod, simply rename/remove `dinput8.dll` from your game's directory.

## DDMK and Crimson

While the randomizer does support loading these two mods up, they also allow for 'cheating' or unintentional bypasses in progression.
There may also be unknown conflicts between either of those mods and my own. 

