import os
import PySimpleGUI as sg
import shutil

sg.theme('DarkBlue')   # Add a touch of color
sg.user_settings_filename(path='.')

settings = sg.UserSettings()
settings.load()
print(settings)
# All the stuff inside your window.
layout = [  [sg.Text('Noita Save File Manager')],
        [sg.Text('Save File Directory: '), sg.Input(settings.get('-folder-name-', ''), key='-IN-'), sg.FolderBrowse()], 
            [sg.Button('Ok', ), sg.Button('Cancel')]]

def get_save_list(dir_path):
    with os.scandir(dir_path) as entries:
        for entry in entries:
            if entry.is_dir() and entry.name == "save00":
                print(f"Found {entry.name} save game")
                shutil.make_archive('test', 'zip', root_dir=dir_path, base_dir=entry.name, dry_run=False)
            else:
                print(f"{entry.name} is not a dir")

# Create the Window
window = sg.Window('Noita Save Manager', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('filebrowsed to', values['-IN-'])
    settings['-folder-name-'] = values['-IN-']
    get_save_list(values['-IN-'])


window.close()
