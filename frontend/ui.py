#!/usr/bin/env python
import PySimpleGUI as sg
from PIL import Image, ImageTk
import io

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

def test_menus():
    sg.theme('LightGrey1')
    sg.set_options(element_padding=(0, 0))

    # ------ Menu Definition ------ #
    menu_def = [
        ['&File', ['&Open     Ctrl-O', '&Save       Ctrl-S', '&Properties', 'E&xit']],
        ['&Edit', ['&Paste', ['Special', 'Normal', ],
                   'Undo', 'Options::this_is_a_menu_key'], ],
        ['&Help', ['&About...']]
    ]

    right_click_menu = ['Unused', [
        'Right', '!&Click', '&Menu', 'E&xit', 'Properties']]


    image_elem = sg.Image(data=get_img_data("C:/Users/MatthewDraws/Pictures/20210914_103416.jpg", first=True))


    # ------ GUI Defintion ------ #
    col2 = sg.Column(
        [[sg.Frame('Tank:', [[sg.Column([[image_elem]])]])]])

    col1 = sg.Column([
        [sg.Text('Auto FRP Tank Calculator',
                 size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('Here is some text.... and a place to enter text')],
        [sg.InputText('This is my text', key='in1')],
        [sg.CBox('Checkbox', key='cb1'), sg.CBox(
            'My second checkbox!', key='cb2', default=True)],
        [sg.Radio('My first Radio!     ', "RADIO1", key='rad1', default=True),
         sg.Radio('My second Radio!', "RADIO1", key='rad2')],
        [sg.MLine(default_text='This is the default Text should you decide not to type anything', size=(35, 3),
                  key='multi1'),
         sg.MLine(default_text='A second multi-line', size=(35, 3), key='multi2')],
        [sg.Combo(('Combobox 1', 'Combobox 2'), key='combo', size=(20, 1)),
         sg.Slider(range=(1, 100), orientation='h', size=(34, 20), key='slide1', default_value=85)],
        [sg.OptionMenu(('Menu Option 1', 'Menu Option 2',
                        'Menu Option 3'), key='optionmenu')],
        [sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3'), size=(30, 3), key='listbox'),
         sg.Slider(range=(1, 100),
                   orientation='v',
                   size=(5, 20),
                   default_value=25, key='slide2', ),
         sg.Slider(range=(1, 100),
                   orientation='v',
                   size=(5, 20),
                   default_value=75, key='slide3', ),
         sg.Slider(range=(1, 100),
                   orientation='v',
                   size=(5, 20),
                   default_value=10, key='slide4')],
        [sg.Text('_' * 80)],
        [sg.Text('Choose A Folder', size=(35, 1))],
        [sg.Text('Your Folder', size=(15, 1), justification='right'),
         sg.InputText('Default Folder', key='folder'), sg.FolderBrowse()],
        [sg.Button('Exit'),
         sg.Text(' ' * 40), sg.Button('SaveSettings'), sg.Button('LoadSettings')]
    ], pad=(0, 0))

    col3 = sg.Column([[sg.Frame('Actions:',
                                [[sg.Column([[sg.Button('Save'), sg.Button('Clear'), sg.Button('Delete'), ]],
                                            size=(450, 45), pad=(0, 0))]])]], pad=(0, 0))

    # The final layout is a simple one
    layout = [[sg.Menu(menu_def, tearoff=True, font='_ 12', key='-MENUBAR-')], [col1, col2],
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

    window.close()


test_menus()
