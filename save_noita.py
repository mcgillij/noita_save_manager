""" Noita Savegame Manager """
import os
import shutil
from datetime import datetime
import PySimpleGUI as sg

SAVE_DIR = "save00"


def find_saves(dir_path):
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
    shutil.move(f"{save_path}/{SAVE_DIR}", f"{save_path}/{backup_dirname}")


def create_save_zip(dir_path):
    with os.scandir(dir_path) as entries:
        for entry in entries:
            if entry.is_dir() and entry.name == SAVE_DIR:
                # uncompressed save game - active
                print(f"Found {entry.name} save game")
                time_string = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
                backup_name = f"noita_backup_{time_string}"
                shutil.make_archive(
                    backup_name,
                    "zip",
                    root_dir=dir_path,
                    base_dir=entry.name,
                    dry_run=False,
                )
            else:
                print(f"{entry.name} is not a dir")


def extract_save(save_dir, backup_dir, zip_filename):
    shutil.unpack_archive(f"{backup_dir}/{zip_filename}", save_dir)


def refresh_save_list():
    window["-listbox-"].update(find_saves(cwd))


if __name__ == "__main__":

    cwd = os.getcwd()
    sg.theme("DarkBlue")  # Add a touch of color
    sg.user_settings_filename(path=f"{cwd}/settings")

    settings = sg.UserSettings()
    settings.load()
    print(settings)

    # find saves
    saves_list = find_saves(cwd)

    USER_PATH = R"% APPDATA %\LocalLow\Nolla_Games_Noita"
    #USER_PATH = "/home/j/gits/save_noita"
    # All the stuff inside your window.
    layout = [
        [
            sg.Text("Noita Directory: "),
            sg.Input(
                settings.get("-folder-name-", os.path.expandvars(USER_PATH)),
                key="-IN-",
                readonly=True),
            sg.FolderBrowse(),
        ],
        [sg.Button("Backup"), sg.Text('<--- backs up current save')],
        [sg.Listbox(
            values=saves_list,
            size=(50, 6),
            key="-listbox-"),
            sg.Button("Select"), sg.Text('<--- restores this backup to active save')],
        [sg.Button("Exit")],
    ]

    # Create the Window
    window = sg.Window("Noita Save Manager", layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):  # if user closes window or clicks Exit
            # exit
            break

        if event == "Select":
            # restore backup
            print("-------in Select -----")
            backup_save_folder(values["-IN-"])
            extract_save(
                values["-IN-"],
                cwd,
                values["-listbox-"].pop()
            )
        elif event == "Backup":
            create_save_zip(values["-IN-"])
            refresh_save_list()

        print(f"------event: {event}, values: {values}")
        print("filebrowsed to", values["-IN-"])
        settings["-folder-name-"] = values["-IN-"]

    window.close()
