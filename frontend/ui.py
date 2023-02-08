#!/usr/bin/env python
import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
import os
from connectors.solidworks import newDoc, closeDoc, createCylinder, setPreferences, openDoc
from connectors.excel import updateValues


def get_img_data(f, maxsize=(1200, 850), first=False):
    """Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)


def app():
    sg.theme('LightGrey1')
    sg.set_options(element_padding=(0, 0))

    # ------ Menu Definition ------ #
    menu_def = [
        ['&File', ['&Open     Ctrl-O', '&Save       Ctrl-S', '&Properties', 'E&xit']],
        ['&Edit', ['&Paste', ['Special', 'Normal', ],
                   'Undo', 'Options::this_is_a_menu_key'], ],
        ['SolidWorks', ['Start SolidWorks', 'New Document',
                        'Close Document', 'Set Preferences']],
        ['&Help', ['&About...']]
    ]

    right_click_menu = ['Unused', [
        'Right', '!&Click', '&Menu', 'E&xit', 'Properties']]

    image_elem = sg.Image(data=get_img_data(
        "C:/Users/draws/Pictures/mountain-lake-landscape-trees-1034377.jpg", first=True))

    # ------ GUI Defintion ------ #
    col2 = sg.Column(
        [[sg.Frame('Tank:', [[sg.Column([[image_elem]])]])]])
    # Tank’s height should be a Dropdown with 4000 6000 8000 and 10000
    col1 = sg.Column([
        # title
        [sg.Text('Auto FRP Tank Calculator',
                 size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('Radius (m):'), sg.Spin(
            values=[i for i in range(0, 1000)], initial_value=350, key='radius', expand_x=True)],
        [sg.Text('Height (cm):'), sg.Combo(
            values=[i for i in range(4000, 10000, 2000)], default_value=6000, key='height', expand_x=True)],
        [sg.Text('Save Tank As:'), sg.Input(key='save_as',
                                                expand_x=True, default_text='auto_frp_tank.prtdot')]
    ], pad=(0, 0))

    col3 = sg.Column([[sg.Frame('Actions:',
                                [[sg.Column([[sg.Button('Go'), sg.Button('Clear'), sg.Button('Delete'), ]],
                                            pad=(0, 0))]])]], pad=(0, 0))

    # The final layout is a simple one
    layout = [[sg.Menu(menu_def, font='_ 12', key='-MENUBAR-')], [col1, col2],
              [col3]]

    window = sg.Window("Auto FRP Tank",
                       layout,
                       resizable=True,
                       right_click_menu=right_click_menu)

    # ------ Loop & Process button menu choices ------ #
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        print(event, values)
        # ------ Process menu choices ------ #
        if event == 'About...':
            window.disappear()
            sg.popup('About this program', 'Version 1.0',
                     'PySimpleGUI Version', sg.get_versions())
            window.reappear()
        elif event == 'Open':
            filename = sg.popup_get_file('file to open', no_window=True)
            print(filename)
        elif event == 'Start SolidWorks':
            print('Starting SolidWorks')
            os.popen('"C:/Program Files/SOLIDWORKS Corp/SOLIDWORKS/SLDWORKS.exe"')
        elif event == 'New Document':
            newDoc()
        elif event == 'Close Document':
            closeDoc()
        elif event == 'Go':
            #createCylinder(float(window.find_element('radius').get()), float(window.find_element('height').get()))
            # update preferences to automatically use excel values
            previousPreference = setPreferences(2)
            # update excel values
            updateValues(float(window.find_element('radius').get()), float(
                window.find_element('height').get()), 100, 100, 750, 400)
            # open part
            openDoc('C:/autofrp/Part1.SLDPRT')
            # revert to previous preference
            setPreferences(previousPreference)
        elif event == 'Clear':
            closeDoc()
        elif event == 'Set Preferences':
            setPreferences(2)

    window.close()


app()
