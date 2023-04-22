#!/usr/bin/env python
import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
import shutil
import time
import os
import traceback
from connectors.solidworks import newDoc, closeDoc, createCylinder, setPreferences, openDoc, saveImage, runStudy
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

    # ------ GUI Defintion ------ #

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
        [sg.Text('Live load (lbf):', pad=(10, 3)),
            sg.Spin(values=[i for i in range(0, 100, 1)], initial_value=0, key='live_load', size=(5, 20))],
        [sg.Text('Dead load (lbf):', pad=(10, 3)),
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
                                   [[sg.Column([[sg.Button('Create Report'), sg.Button('Create Model'), sg.Button('Run Simulation'), sg.Text('Tank Name:', pad=(10, 3)), sg.InputText(key='tank_name', size=(20, 20))]],
                                               pad=(0, 0))]])]], pad=(0, 0))

    layout = [
        [sg.Menu(menu_def, font='_ 12', key='-MENUBAR-')],
        [[sg.TabGroup([[sg.Tab('Features', features), sg.Tab('Environment', environment), sg.Tab('Contents', contents),
                        sg.Tab('Top Head', top_head), sg.Tab('Shell', shell),]],
                      key='-TAB GROUP-', expand_x=True, expand_y=True),]], [actions]]

    window = sg.Window("Auto FRP Tank", layout, resizable=True,
                       right_click_menu=right_click_menu, icon=b'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')

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
                if values['tank_name'] == '':
                    filename = sg.popup_get_file(
                        'file to save', no_window=True, save_as=True, file_types=(('HTML Files', '*.html'),))
                    values['tank_name'] = filename.split('/')[-1].split('.')[0]
                    window['tank_name'].update(values['tank_name'])
                else:
                    filename = f'{values["tank_name"]}.html'
                # calculate tank
                exportResults(filename, calculateTank(values))
            except Exception as e:
                print(traceback.format_exc())
                sg.popup('Error', e)
        elif event == 'Create Model':
            try:
                if values['tank_name'] == '':
                    filename = sg.popup_get_file(
                        'file to save', no_window=True, save_as=True, file_types=(('HTML Files', '*.html'),))
                    values['tank_name'] = filename.split('/')[-1].split('.')[0]
                    window['tank_name'].update(values['tank_name'])
                else:
                    filename = f'{values["tank_name"]}.html'
                # calculate tank
                exportResults(filename, calculateTank(values))
                # close any open documents
                closeDoc()
                time.sleep(2)
                # calculate tank
                tank = calculateTank(values)
                # createCylinder(float(window.find_element('diameter').get()), float(window.find_element('height').get()))
                # update preferences to automatically use excel values
                previousPreference = setPreferences(2)
                # update excel values
                updateValues(25.4*float(tank['height']), 25.4*(float(
                    tank['diameter']) + float(tank['thickness'])), 25.4*float(tank['diameter']))
                file = f'{values["top_head"]}_Head_{"Wood" if values["bottom_head"] == "Balsa Wood Core" else values["bottom_head"]}_Bottom'
                # Move file to exec directory
                shutil.copy(
                    f'C:/autofrp/models/{file}.SLDPRT', f'C:/autofrp/{file}.SLDPRT')
                shutil.copy(
                    f'C:/autofrp/models/{file}-Static 1.CWR', f'C:/autofrp/{file}-Static 1.CWR')
                # open part
                openDoc(f'C:/autofrp/{file}.SLDPRT')
                # revert to previous preference
                setPreferences(previousPreference)
            except Exception as e:
                print(e)
                sg.popup('Error', e)
        elif event == 'Run Simulation':
            try:
                # calculate tank
                tank = calculateTank(values)
                runStudy(float(tank['thickness']), -1*float(tank['internal_pressure']),
                         float(tank['external_pressure']))
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
