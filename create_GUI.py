# -*- coding: utf-8 -*-
"""
The GUI application
Code to create an .exe program to get all input from the user of the application.

Harmen Dijkstra, 29-11-2021
"""

import PySimpleGUI as sg
import sys

weapons = ['de lepel', 'de vork', 'het mes', 'de pen', 'het boek', 'het keyboard',
             'de sleutel', 'het kussen', 'de kleerhanger', 'de jas', 'de sleutel',
             'het potlood', 'de schaar', 'het schilmesje', 'de schoen', 'het bierflesje',
             'de beker', 'de bezem', 'de handdoek', 'de zeep', 'het beeldje',
             'de klok', 'het touw', 'de washand', 'de corona sneltest', 'een vies koekje']

locations = ['achtertuin', 'woonkamer', 'keuken', 'gang',
             'studeer', 'zolder', 'badkamer', 'overloop', 
             'voortuin', 'slaapkamer 1', 'slaapkamer 2',
             'slaapkamer 3', 'slaapkamer 4', 'wc', 'bijkeuken']

def gui_input():
    sg.ChangeLookAndFeel('DarkAmber')

    layout = [
        
        [sg.Text('Vul alle emailadressen in:')],
        [sg.Multiline(size=(60, 5), key='emails')],
        
        [sg.Text('Aantal moordenaars:')],
        [sg.InputCombo(('1', '2', '3', '4', '5'), size=(20, 3), key='nr_killers')],

        [sg.Text('Tenminste x personen bij de moordenaars:')],
        [sg.InputCombo(('1', '2', '3', '4', '5'), size=(20, 3), key='knowledge_people')],
        
        [sg.Text('Maximaal x personen bij niet moordenaars:')],
        [sg.InputCombo(('1', '2', '3', '4', '5'), size=(20, 3), key='max_persons')],

        [sg.Text('Moordenaars kennen elkaar:')],
        [sg.InputCombo(('Ja', 'Nee'), size=(20, 2), key='knowledge')],

        [sg.Text('Kies de wapens (met control kan je meer kiezen)')],
        [sg.Listbox(values = list(weapons), select_mode='extended', key='weapons', size=(20, 8))],
        
        [sg.Text('Kies de locaties (met control kan je meer kiezen)')],
        [sg.Listbox(values = list(locations), select_mode='extended', key='locations', size=(20, 8))],

        [sg.Submit(font=('Times New Roman', 18)), sg.Cancel(font=('Times New Roman', 18))]
        ]
    
    form = sg.FlexForm('Moord in Loppersum', layout, default_element_size=(40, 1))

    #TODO, crash bij cancel!
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

                if values['knowledge'] == '':
                    event = 'Error'
                    values['exception'] = 'knowledge'
                    sg.Popup('oops! Je moet opgeven of de moordenaars elkaar kennen')
                    continue

                if values['max_persons'] == '':
                    event = 'Error'
                    values['exception'] = 'max_persons'
                    sg.Popup('oops! Je moet maximaal x aantal personen bij de niet moordenaars opgeven.')
                    continue

                if values['knowledge_people'] == '':
                    event = 'Error'
                    values['exception'] = 'knowledge_people'
                    sg.Popup('oops! Je moet x aantal personen opgeven')
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