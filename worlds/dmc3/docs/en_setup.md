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

Note: The mod will not load hooks for DDMK if it is not version 2.7.3 from Github. Additionally, while the mod will not stop itself from loading if DMC3 is not properly patched. Issues or crashes will most likely occur.
## 2. Install the randomizer.
If you already have a `dinput8.dll` from another mod, rename it to something else and extract the randomizers `dinput8.dll` into the same directory as `dmc3.exe` 

The randomizer will load up DDMK or Crimson if it is installed. 

Note: If you have another mod that uses `dinput8.dll` to load up, please let me know and I can try to make it so the rando will load it as well upon start.

If the mod has been successfully installed, when start up DMC3 and you should have a console window and potentially a modified DDMK overlay. 

## 3. Connect to a room
It is recommended that before launching DMC3, you start up the DMC3 Client available in the Archipelago launcher. This launcher is what you use to connect to the room.

Once the client is connected, start up Devil May Cry 3, it should then connect to the Archipelago client. You can use the command "/dmc3" in the Archipelago client to verify that it is connected

If for some reason the mod doesn't seem to be connecting despite correct information, try restarting the game.

Then you may start at Mission #1.
## 4. Start up DMC3 straight from the exe file

There is a `steam_appid.txt` file in the zip, put this in the same place as your `dmc3.exe`, this will allow you to start up DMC3 from its EXE and skip the launcher. While technically this should be optional, people have reported that the mod acts up without the file.

This also works for the same for DMC1 and 2, DMC2 however will default to Dante unless launched with `lucia` as an argument.

I.e A shortcut to DMC2 that is setup with this as the `Target`

```"C:\Program Files (x86)\Steam\steamapps\common\Devil May Cry HD Collection\dmc2.exe" lucia```

## Uninstallation

To disable/remove the mod, simply rename/remove `dinput8.dll` from your game's directory.

## DDMK and Crimson

While the randomizer does support loading these two mods up, they also allow for 'cheating' or unintentional bypasses in progression.
There may also be unknown conflicts between either of those mods and my own. 

## Linux/Steam Deck notes
(Steam deck support is entirely untested since I do not own one, but should hypothetically work)

DDMK needs a font called "consolas"/consola.ttf to be available. DDMK may also fail to display its GUI while running through the mod. 

To load up the randomizer on Linux set your steam launch arguments to this
`WINEDLLOVERRIDES="dinput8=n" %command%`
