""" Noita Savegame Manager """
import os
import shutil
from datetime import datetime

import psutil
import PySimpleGUI as sg

SAVE_DIR = "save00"
DEBUG = False
# sg Debug window
if os.environ.get("DEBUG") or DEBUG:
    print = sg.Print


# def is_noita_running():
#    for process in psutil.process_iter():
#        try:
#            if "noita.exe".lower() in process.name().lower():
#                return True
#        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#            pass
#    return False


def find_save_zips(dir_path):
    saves = []
    if dir_path:
        for file in os.listdir(dir_path):
            if file.endswith(".zip"):
                print(f"{file} found and is a .zip save")
                saves.append(file)
    return saves


def backup_save_folder(save_path):
    # check if dir already exists, if not move
    timestamp = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    backup_dirname = f"{SAVE_DIR}.{timestamp}.bak"
    save_dirname = f"{save_path}/{SAVE_DIR}"
    if os.path.exists(save_dirname):
        shutil.move(save_dirname, f"{save_path}/{backup_dirname}")
        # create empty dir in it's place.
    make_save_dir(save_dirname)


def make_save_dir(save_dirname):
    try:
        os.mkdir(save_dirname)
    except OSError:
        print("could not create the dir %s failed" % save_dirname)
    else:
        print("directory created succesfully")


def create_save_zip(dir_path):
    # uncompressed save game - active
    time_string = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    backup_name = f"noita_backup_{time_string}"
    shutil.make_archive(
        backup_name,
        "zip",
        root_dir=dir_path,
        base_dir=SAVE_DIR,
        dry_run=False,
    )
    print("Backup created")


def extract_save(save_dir, backup_dir, zip_filename):
    shutil.unpack_archive(f"{backup_dir}/{zip_filename}", save_dir)
    print("Restored from backup")


def main():
    def refresh_save_list():
        window["-listbox-"].update(find_save_zips(cwd))

    cwd = os.getcwd()
    sg.theme("DarkBlue")  # Add a touch of color
    sg.user_settings_filename(path=f"{cwd}/settings")

    settings = sg.UserSettings()
    settings.load()

    # find saves
    saves_list = find_save_zips(cwd)

    # Check if running in Windows
    if os.name == "nt":
        print("Running in Windows")
        user_path = R"C:\Users\%username%\AppData\LocalLow\Nolla_Games_Noita"
    else:
        print("Running in Linux")
        user_path = "/home/j/gits/save_noita"

    layout = [
        [
            sg.Text("Noita Directory: "),
            sg.Input(
                settings.get("-folder-name-", os.path.expandvars(user_path)),
                key="-IN-",
                readonly=True,
            ),
            sg.FolderBrowse(),
        ],
        [sg.Button("Backup"), sg.Text("<--- backs up current save")],
        [
            sg.Listbox(values=saves_list, size=(50, 6), key="-listbox-"),
            sg.Button("Select"),
            sg.Text("<--- restores this backup to active save"),
        ],
        [sg.Button("Exit")],
    ]

    # Create the Window
    window = sg.Window("Noita Save Manager", layout)

    # Event loop
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):  # if user closes window or clicks Exit
            # exit
            break
        # if is_noita_running():
        #    # Noita must not be running during backup
        #    print("please close noita before using this")
        #    continue
        if event == "Select":
            # restore backup
            if values["-listbox-"]:
                backup_save_folder(values["-IN-"])
                extract_save(values["-IN-"], cwd, values["-listbox-"].pop())
            else:
                print("Please select a backups to restore")
        elif event == "Backup":
            if os.path.exists(values["-IN-"]):
                create_save_zip(values["-IN-"])
                refresh_save_list()
            else:
                print("There's nothing to backup")

        # save the folder to the settings
        settings["-folder-name-"] = values["-IN-"]

    window.close()


if __name__ == "__main__":
    main()
