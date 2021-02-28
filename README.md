# Noita save manager

Small save-game manager written for usage with Noita.

# Screenshot

![Noita save manager](https://raw.githubusercontent.com/mcgillij/noita_save_manager/main/images/noita_save_manager.png)

# Features
* Check to see if Noita is running
* Backup active save
* Restore from backup
* Non destructive

# Non Destructive
Currently you cannot use this tool to delete / remove saves or backups.
It will always create a backup in the Noita folder prior to restoring. So it won't overwrite / delete anything.

# Debugging

Currently this version has a debugging window enabled to make sure everything's working correctly.

# Download

You can grab the latest release https://github.com/mcgillij/noita_save_manager/releases/download/0.1.0/save_manager_0.1.0.zip

# Building from source

If you want to build your own binary/ source distribution / wheel, you can use the following steps. Uses **poetry** for dependency management.

``` bash
poetry install
poetry run pyinstaller -F --noconsole save_manager/save_manager.py
```

This will plop out a binary for you in the `dist/` folder.
