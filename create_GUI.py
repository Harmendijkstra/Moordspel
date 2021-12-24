# -*- coding: utf-8 -*-
"""
The GUI application
Code to create an .exe program to get all input from the user of the application.

Harmen Dijkstra, 29-11-2021
"""

import PySimpleGUI as sg
import sys

weapons = ['lepel', 'vork', 'mes', 'pen', 'boek', 'pan',
             'sleutel', 'kussen', 'kleerhanger', 'jas',
             'potlood', 'schaar', 'schilmesje', 'schoen',
             'beker', 'bezem', 'handdoek', 'zeep', 'beeldje',
             'klok', 'touw', 'washand', 'corona sneltest', 'vies koekje']
locations = ['tuin', 'woonkamer', 'keuken', 'gang',
             'studeer', 'zolder', 'badkamer', 'overloop', 
             'voor het huis', 'slaapkamer 1', 'slaapkamer 2',
             'slaapkamer 3', 'slaapkamer 4', 'wc', 'bijkeuken']

def gui_input():
    checked_eforms = False

    sg.ChangeLookAndFeel('DarkAmber')

    layout = [
        
        [sg.Text('Vul alle emailadressen in:')],
        [sg.Multiline(size=(60, 5), key='emails')],
        
        [sg.Text('Aantal moordenaars:')],
        [sg.InputCombo(('1', '2', '3', '4', '5'), size=(20, 3), key='nr_killers')],

        [sg.Text('Kies de wapens (met control kan je meer kiezen)')],
        [sg.Listbox(values = list(weapons), select_mode='extended', key='weapons', size=(20, len(list(weapons))))],
        
        [sg.Text('Kies de locaties (met control kan je meer kiezen)')],
        [sg.Listbox(values = list(locations), select_mode='extended', key='locations', size=(20, len(list(locations))))],

        [sg.Submit(font=('Times New Roman', 18)), sg.Cancel(font=('Times New Roman', 18))]
        ]
    
    form = sg.FlexForm('Moord in Loppersum', layout, default_element_size=(40, 1))

    
    while True:
        event, values = form.Read()
        values['event'] = event
        values['exception'] = 'None'
        print('event:', event)
        print('values:', values)
        
        if (event == 'Cancel') or (event == sg.WIN_CLOSED):
            break
            
        elif event == 'Submit':
            try:
                emails_all = values['emails'].split('\n')
                input_emails = list(filter(None, emails_all)) 
                input_locations = values['locations']
                input_weapons = values['weapons']
                 
                if values['weapons'] == '':
                    event = 'Error'
                    values['exception'] = 'weapons'
                    sg.Popup('oops! Je moet de wapens nog kiezen')
                    continue

                if values['locations'] == '':
                    event = 'Error'
                    values['exception'] = 'locations'
                    sg.Popup('oops! Je moet de locaties nog kiezen')
                    continue

                if values['nr_killers'] == '':
                    event = 'Error'
                    values['exception'] = 'nr_killers'
                    sg.Popup('oops! Je moet het aantal moordenaars nog kiezen')
                    continue
                
                if values['emails'] == '':
                    event = 'Error'
                    values['exception'] = 'emails'
                    sg.Popup('oops! Je moet de emails nog kiezen')
                    continue
                



                nr_items = len(input_emails) + len(input_locations) + len(input_weapons)
                nr_remaining_items = 3*len(input_emails) + 2 + int(values['nr_killers'])
                if nr_items != nr_remaining_items:
                    event = 'Error'
                    values['exception'] = 'wrong number of items'
                    sg.Popup(f'oops! Het aantal wapens+locaties+emails (nu: {nr_items}) moet gelijk zijn aan 3*aantal emails - 3 - aantal moordenaars (nu: {nr_remaining_items})')
                    continue
                


            except Exception as e:
                event = 'Error'
                sg.Popup('oops! En error occured', e)
                form.close()
                sys.exit
            else:
                break
            
    form.close()
    sys.exit
    
    return values