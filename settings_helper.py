import configparser
from tkinter import Tk
from tkinter.filedialog import askdirectory

config = configparser.ConfigParser()

config = configparser.ConfigParser()
config.read('config.ini')

default_output = config['UserSettings']['default_output']
download_folder = config['UserSettings']['download_folder']

def prompt_settings():
    print('================================================================================')
    print('                                 Settings')
    print('================================================================================')
    print()
    print('[1]. Change default output')
    print('[2]. Change download folder')
    print('[3]. Exit and run program')
    print()
    user_input = input('Enter a number: ')
    if user_input == '1':
        change_default_output()
        prompt_settings()
    elif user_input == '2':
        change_download_folder()
        prompt_settings()
    elif user_input == '3' or user_input == 'exit':
        pass
    else:
        print('Invalid input, please choose a number from the list above.')
        prompt_settings()

def change_default_output():
    # Print options:
    print('Enter new default output')
    print('1. [w]rite to file')
    print('2. [c]opy to clipboard')
    print('3. [a]sk each time (default)')
    res = input('Enter decision: ')

    # Check user input
    if res.strip().lower() == 'w':
        new_output = 'file'
    elif res.strip().lower() == 'c':
        new_output = 'clipboard'
    elif res.strip().lower() == 'a':
        new_output = 'ask'
    elif res.strip().lower() == 'clear':
        new_output = ''
    else:
        print('Invalid input. Please respond with [w], [c] or [a].')
        change_default_output()
    
    # Write new default output to config file
    config['UserSettings']['default_output'] = new_output
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print(f"Default output changed -> {new_output}")

def change_download_folder():
    path = askdirectory(title='Select Folder') # shows dialog box and return the path
    
    config['UserSettings']['download_folder'] = path
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("Download folder changed to: " + path)

def get_download_folder():
    return download_folder

def get_default_output():
    return default_output