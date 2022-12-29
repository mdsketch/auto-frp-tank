#!/usr/bin/env python
import PySimpleGUI as sg
from PIL import Image, ImageTk
import io, os
from connectors.solidworks import newDoc, closeDoc


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
        ['SolidWorks', ['Start SolidWorks', 'New Document', 'Close Document']],
        ['&Help', ['&About...']]
    ]

    right_click_menu = ['Unused', [
        'Right', '!&Click', '&Menu', 'E&xit', 'Properties']]

    image_elem = sg.Image(data=get_img_data(
        "C:/Users/draws/Pictures/mountain-lake-landscape-trees-1034377.jpg", first=True))

    # ------ GUI Defintion ------ #
    col2 = sg.Column(
        [[sg.Frame('Tank:', [[sg.Column([[image_elem]])]])]])

    col1 = sg.Column([
        # title
        [sg.Text('Auto FRP Tank Calculator',
                 size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('Radius (m):'), sg.Spin(
            values=[i for i in range(0, 1000)], initial_value=100, key='radius', expand_x=True)],
        [sg.Text('Height (m):'), sg.Spin(
            values=[i for i in range(0, 1000)], initial_value=100, key='height', expand_x=True)]
    ], pad=(0, 0))

    col3 = sg.Column([[sg.Frame('Actions:',
                                [[sg.Column([[sg.Button('Save'), sg.Button('Clear'), sg.Button('Delete'), ]],
                                            size=(450, 45), pad=(0, 0))]])]], pad=(0, 0))

    # The final layout is a simple one
    layout = [[sg.Menu(menu_def, font='_ 12', key='-MENUBAR-')], [col1, col2],
              [col3]]

    window = sg.Window("Auto FRP Tank",
                       layout,
                       default_element_size=(12, 1),
                       default_button_element_size=(12, 1),
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

    window.close()


app()
