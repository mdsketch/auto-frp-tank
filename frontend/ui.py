#!/usr/bin/env python
import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
import os
import traceback
from connectors.solidworks import newDoc, closeDoc, createCylinder, setPreferences, openDoc, saveImage
from connectors.excel import updateValues
from connectors.data import saveSettings, loadSettings, exportResults
from connectors.formulas import calculateTank

environmental_vars = {
    'snow': {"name": "Snow Pressure",
             "fields": ['Ce', 'Ct', 'Is', 'Pg'],
             },
    'wind': {"name": "Wind Pressure",
             "fields":  ['q', 'qi', 'qh', 'G', 'Cp', 'GCpi'],
             },
    'seismic': {"name": "Seismic:",
                "fields": ['Ss', 'S1', 'Fv', 'Fa', 'Tl'],
                },
}


def get_img_data(f, maxsize=(800, 800), first=False):
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
        ['&File', ['&Open', '&Save', '&Properties', 'E&xit']],
        ['&Edit', ['&Paste', ['Special', 'Normal', ],
                   'Undo', 'Options::this_is_a_menu_key'], ],
        ['SolidWorks', ['Start SolidWorks', 'New Document',
                        'Close Document', 'Set Preferences']],
        ['&Help', ['&About...']]
    ]

    right_click_menu = ['Unused', [
        'Right', '!&Click', '&Menu', 'E&xit', 'Properties']]

    image_elem = sg.Image(data=get_img_data(
        "C:/autofrp/solidworx.jpg", first=True))

    # ------ GUI Defintion ------ #
    image = sg.Column(
        [[sg.Frame('Tank:', [[sg.Column([[image_elem]])]])]])

    # Main tank tab
    features = [
        [sg.Text('Tank Internal Diameter (in):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 144, 1)], initial_value=36, key='diameter', size=(5, 20))],
        [sg.Text('Tank Height (in):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 10000, 1)], initial_value=76, key='height', size=(5, 20))],
        [sg.Text('Internal Pressure (psi):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 15, 1)], initial_value=0, key='internal_pressure', size=(5, 20))],
        [sg.Text('External Pressure (psi):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 15, 1)], initial_value=0, key='external_pressure', size=(5, 20))],
        [sg.Text('Tank Type:', pad=(10, 3)),
         sg.Combo(values=['FRP', 'Dual Laminate'], default_value='FRP', key='tank_type', size=(20, 20), enable_events=True)],
        [sg.Text('Bottom Head Type:', pad=(10, 3)),
            sg.Combo(values=['Torispherical', 'Conical', 'Hemispherical', 'Flat', 'Balsa Wood Core'], default_value='Flat', key='bottom_head', size=(20, 20))],
        [sg.Text('Ignore Corrosion Barrier:', pad=(10, 3)),
            sg.Checkbox('', key='corrosion_barrier', default=True, enable_events=True)],
        [sg.Text('Corrosion Barrier Thickness (in):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 15, 1)], initial_value=0, key='corrosion_barrier_thickness', size=(5, 20), disabled=True)],
        [sg.Text('Corrosion Liner Thickness (in):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 15, 1)], initial_value=0, key='corrosion_liner_thickness', size=(5, 20), disabled=True)],
    ]

    # Environment tab
    environment = [
        [sg.Text('Tensile Operating Force (lbf):', pad=(10, 3)),
            sg.Checkbox('', key='tensile_force', enable_events=True),
            sg.Spin(values=[i for i in range(0, 15, 1)], initial_value=0, key='tensile_force_value', size=(5, 40), disabled=True)],
        [sg.Text('Operating Moment (in-lb):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 15, 1)], initial_value=0, key='operating_moment', size=(5, 40), disabled=True)],
        [sg.Text('Is tank outside?', pad=(10, 3)),
            sg.Checkbox('', key='outdoor', default=False, enable_events=True)],
        [sg.Text('Compressive Operating Force (in-lb):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 15, 1)], initial_value=0, key='compressive_force', size=(5, 20), disabled=True)],

    ]
    # dynamic environment
    for key, value in environmental_vars.items():
        spinners = []
        # add fields and spinners
        for field in value['fields']:
            spinners.append(sg.Text(text=field, pad=(10, 3)))
            spinners.append(sg.Spin(values=[i for i in range(
                0, 15, 1)], initial_value=0, key=f'{key}_{field}', size=(5, 20), disabled=True))
        # add to correct row in environment tab
        environment.append([sg.Text(value['name'], pad=(10, 3)),
                            sg.Checkbox('', key=key, default=False,
                                        enable_events=True),
                            *spinners])

    # Tank contents tab
    contents = [
        [sg.Text('Storage Type:', pad=(10, 3)),
         sg.Combo(values=['Liquid', 'Gas'], default_value='Gas',
                  key='storage_type', size=(10, 20), enable_events=True),
         sg.Text('Specific Gravity:', pad=(10, 3),
                 key='specific_gravity_text'),
            sg.Spin(values=[i for i in range(0, 15, 1)], initial_value=0, key='specific_gravity', size=(5, 20), disabled=True)],
        [sg.Text('Height of Liquid (in):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 15, 1)], initial_value=0, key='liquid_height', size=(5, 20))],
    ]

    # Top Head
    top_head = [
        [sg.Text('Type:', pad=(10, 3)),
            sg.Combo(values=['Torispherical', 'Ellipsoidal', 'Flat'], default_value='Flat', key='top_head', size=(20, 20))],
        [sg.Text('Live load (kN/m2):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 100, 1)], initial_value=0, key='live_load', size=(5, 20))],
        [sg.Text('Dead load (kN/m2):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 100, 1)], initial_value=0, key='dead_load', size=(5, 20))],
    ]

    # Shell
    shell = [
        [sg.Text('Type:', pad=(10, 3)),
            sg.Combo(values=['Hand Lay-Up', 'Filament Wound'], default_value='Hand Lay-Up', key='shell', size=(20, 20))],
        [sg.Text('Hoop Tensile Modulus (psi):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 100, 1)], initial_value=0, key='hoop_tensile_modulus', size=(5, 20))],
        [sg.Text('Hoop Tensile Strength (psi):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 100, 1)], initial_value=0, key='hoop_tensile_strength', size=(5, 20))],
        [sg.Text('Axial Tensile Modulus (psi):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 100, 1)], initial_value=0, key='axial_tensile_modulus', size=(5, 20))],
        [sg.Text('Axial Tensile Strength (psi):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 100, 1)], initial_value=0, key='axial_tensile_strength', size=(5, 20))],
    ]

    actions = sg.Column([[sg.Frame('Actions:',
                                   [[sg.Column([[sg.Button('Create Report'), sg.Button('Create Model'), sg.Button('Delete'), ]],
                                               pad=(0, 0))]])]], pad=(0, 0))

    layout = [
        [sg.Menu(menu_def, font='_ 12', key='-MENUBAR-')],
        [[sg.TabGroup([[sg.Tab('Features', features), sg.Tab('Environment', environment), sg.Tab('Contents', contents),
                        sg.Tab('Top Head', top_head), sg.Tab('Shell', shell),]],
                      key='-TAB GROUP-', expand_x=True, expand_y=True),]], [actions], [image]]

    window = sg.Window("Auto FRP Tank", layout, resizable=True,
                       right_click_menu=right_click_menu)

    # TODO: add error handling for specific cases
    # have 1 large try except for all events and display error message according to the error type
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        print(event, values)
        # Functional Events
        if event == 'About...':
            window.disappear()
            sg.popup('About this program', 'Version 1.0',
                     'PySimpleGUI Version', sg.get_versions())
            window.reappear()
        elif event == 'Open':
            try:
                filename = sg.popup_get_file(
                    'file to open', no_window=True)
                settings = loadSettings(filename)
                # update keys with settings
                for key in settings:
                    window[key].update(settings[key])
            except Exception as e:
                print(e)
                sg.popup('Open Failed')
        elif event == 'Save':
            try:
                filename = sg.popup_get_file(
                    'file to save', no_window=True, save_as=True)
                # save settings remove -MENUBAR- and -TAB GROUP-
                values.pop('-MENUBAR-')
                values.pop('-TAB GROUP-')
                saveSettings(filename, values)
            except Exception as e:
                print(e)
                sg.popup('Save Failed')
        elif event == 'Start SolidWorks':
            try:
                print('Starting SolidWorks')
                os.popen(
                    '"C:/Program Files/SOLIDWORKS Corp/SOLIDWORKS/SLDWORKS.exe"')
            except Exception as e:
                print(e)
                sg.popup('SolidWorks Failed to Start')
        elif event == 'New Document':
            try:
                newDoc()
            except Exception as e:
                print(e)
                sg.popup('New Document Failed')
        elif event == 'Close Document':
            closeDoc()
        elif event == 'Create Report':
            try:
                # calculate tank
                exportResults("test.html", calculateTank(values))
            except Exception as e:
                print(traceback.format_exc())
                sg.popup('Error', e)
        elif event == 'Create Model':
            try:
                # calculate tank
                tank = calculateTank(values)
                # createCylinder(float(window.find_element('diameter').get()), float(window.find_element('height').get()))
                # update preferences to automatically use excel values
                previousPreference = setPreferences(2)
                # update excel values
                updateValues(float(window.find_element('diameter').get()), float(
                    window.find_element('height').get()), 100, 100, 750, 400)
                # open part
                openDoc('C:/autofrp/Part1.SLDPRT')
                # revert to previous preference
                setPreferences(previousPreference)
                saveImage()
                # set 'C:\\autofrp\\doc1.png' as image
                image_elem.update(data=get_img_data(
                    "C:/autofrp/doc1.png", first=False))
            except Exception as e:
                print(e)
                sg.popup('Error', e)
        elif event == 'Clear':
            try:
                closeDoc()
            except:
                sg.popup('Clear Failed')
        elif event == 'Set Preferences':
            try:
                setPreferences(2)
            except:
                sg.popup('Set Preferences Failed')
        # UI events
        elif event == 'storage_type':
            if values['storage_type'] == 'Liquid':
                window.find_element('specific_gravity').update(disabled=False)
            else:
                window.find_element('specific_gravity').update(disabled=True)
        elif event == 'snow':
            for value in environmental_vars['snow']['fields']:
                window.find_element(f'snow_{value}').update(
                    disabled=not values['snow'])
        elif event == 'wind':
            for value in environmental_vars['wind']['fields']:
                window.find_element(f'wind_{value}').update(
                    disabled=not values['wind'])
        elif event == 'seismic':
            for value in environmental_vars['seismic']['fields']:
                window.find_element(f'seismic_{value}').update(
                    disabled=not values['seismic'])
        elif event == 'tensile_force':
            window.find_element('tensile_force_value').update(
                disabled=not values['tensile_force'])
            if not values['outdoor']:
                window.find_element(
                    'operating_moment').update(disabled=not values['tensile_force'])
        elif event == 'corrosion_barrier':
            window.find_element('corrosion_barrier_thickness').update(
                disabled=values['corrosion_barrier'])
            window.find_element('corrosion_liner_thickness').update(
                disabled=values['corrosion_barrier'])
            if values['tank_type'] == 'FRP':
                window.find_element('corrosion_liner_thickness').update(
                    disabled=True)
                window.find_element('corrosion_liner_thickness').update(
                    value=0)
        elif event == 'tank_type':
            if (not values['corrosion_barrier']):
                if values['tank_type'] == 'Dual Laminate':
                    window.find_element('corrosion_liner_thickness').update(
                        disabled=False)
                else:
                    window.find_element('corrosion_liner_thickness').update(
                        disabled=True)
                    window.find_element('corrosion_liner_thickness').update(
                        value=0)
        elif event == 'outdoor':
            elements = ['compressive_force', 'operating_moment']
            if values['tensile_force']:
                elements.remove('operating_moment')
            for element in elements:
                window.find_element(element).update(
                    disabled=not values['outdoor'])
            # update all environmental fields as well
            for env in environmental_vars:
                window.find_element(env).update(value=values['outdoor'])
                for value in environmental_vars[env]['fields']:
                    window.find_element(f'{env}_{value}').update(
                        disabled=not values['outdoor'])

    window.close()


app()
