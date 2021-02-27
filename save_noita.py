import os
import PySimpleGUI as sg
import shutil
from datetime import datetime

sg.theme('DarkBlue')   # Add a touch of color
sg.user_settings_filename(path='.')

settings = sg.UserSettings()
settings.load()
print(settings)

SAVE_DIR_NAME = "save00"

def find_saves(dir_path):
    saves = []
    if dir_path:
        for file in os.listdir(dir_path):
            if file.endswith(".zip"):
                print(f"{file} found and is a .zip save")
                saves.append(file)
    return saves

# find saves
saves = find_saves(settings.get('-backups-folder-name-'))

# All the stuff inside your window.
layout = [ [sg.Text('Save File Directory: '), sg.Input(settings.get('-folder-name-', ''), key='-IN-', readonly=True), sg.FolderBrowse()],
           [sg.Text('Backups Directory: '), sg.Input(settings.get('-backups-folder-name-', ''), key='-BACKUPS-', readonly=True), sg.FolderBrowse()],
           [sg.Button('Backup')],
           [sg.Listbox(values=saves, size=(50, 6), key='-listbox-'), sg.Button('Select')],
           [sg.Button('Exit')]]


def backup_save_folder(save_path):
    # check if dir already exists, if not move
    timestamp = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    backup_dirname = f"{SAVE_DIR_NAME}.{timestamp}.bak"
    shutil.move(f"{save_path}/{SAVE_DIR_NAME}", f"{save_path}/{backup_dirname}")


def create_save_zip(dir_path):
    with os.scandir(dir_path) as entries:
        for entry in entries:
            if entry.is_dir() and entry.name == SAVE_DIR_NAME:
                # uncompressed save game - active
                print(f"Found {entry.name} save game")
                time_string = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
                backup_name = f"noita_backup_{time_string}"
                shutil.make_archive(backup_name, 'zip', root_dir=dir_path, base_dir=entry.name, dry_run=False)
            else:
                print(f"{entry.name} is not a dir")


def extract_save(save_dir, backup_dir, save_zip_file):
    shutil.unpack_archive(f"{backup_dir}/{save_zip_file}", save_dir)

def refresh_save_list():
    window['-listbox-'].update(find_saves(values['-BACKUPS-']))


# Create the Window
window = sg.Window('Noita Save Manager', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks Exit
        # exit
        break
    elif event == 'Select':
        # restore backup
        print("-------in Select -----")
        backup_save_folder(values['-IN-'])
        extract_save(values['-IN-'], values['-BACKUPS-'], values['-listbox-'].pop())
    elif event == "Backup":
        create_save_zip(values['-IN-'])
        refresh_save_list()

    print(f"------event: {event}, values: {values}")
    print('filebrowsed to', values['-IN-'])
    settings['-folder-name-'] = values['-IN-']
    settings['-backups-folder-name-'] = values['-BACKUPS-']
    saves = find_saves(values['-BACKUPS-'])
    print(f"{saves} - saves")


window.close()
