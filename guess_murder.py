# -*- coding: utf-8 -*-
"""
The GUI application
Code to create an .exe program to get all input from the user of the application.

Harmen Dijkstra, 29-11-2021
"""

import PySimpleGUI as sg
import sys
import pandas as pd
from read_input import read_input_excel

df_weapons = read_input_excel('Secretinfo.xlsx', 'Weapons')
df_locations = read_input_excel('Secretinfo.xlsx', 'Locations')
df_emails = read_input_excel('Secretinfo.xlsx', 'Emails')
df_murder = read_input_excel('Secretinfo.xlsx', 'Murder')

weapons = list(df_weapons[0])
locations = list(df_locations[0])
emails = list(df_emails[0])



def gui_input():
    sg.ChangeLookAndFeel('DarkAmber')

    layout = [
        [sg.Text('Kies moordwapen:')],
        [sg.Combo(weapons, size=(20, len(weapons)), key='weapons')],

        [sg.Text('Kies locatie:')],
        [sg.Combo(locations, size=(20, len(locations)), key='locations')],
        
        #TODO aantal moordenaars afhankelijk van input!!!
        [sg.Text('Kies moordenaar 1 (volgorde moordenaar maakt niet uit, kies wel verschillende):')],
        [sg.Combo(emails, size=(20, len(emails)), key='moordenaar1')],

        [sg.Text('Kies moordenaar 2:')],
        [sg.Combo(emails, size=(20, len(emails)), key='moordenaar2')],

        [sg.Submit(font=('Times New Roman', 18)), sg.Cancel(font=('Times New Roman', 18))]
        ]
    
    form = sg.FlexForm('Moord gegevens', layout, default_element_size=(40, 1))

    
    while True:
        event, values = form.Read()
        values['event'] = event
        values['exception'] = 'None'
        print('event:', event)
        print('values:', values)
        
        if (event == 'Cancel') or (event == sg.WIN_CLOSED):
            break
            
        elif event == 'Submit':
            chosen_weapon = values['weapons']
            chosen_location = values['weapons']
            chosen_moordenaar1 = values['moordenaar1']
            chosen_moordenaar2 = values['moordenaar2']
            try: 
                if values['weapons'] == '':
                    event = 'Error'
                    values['exception'] = 'weapons'
                    sg.Popup('oops! Je moet het wapen nog kiezen')
                    continue

                if values['locations'] == '':
                    event = 'Error'
                    values['exception'] = 'locations'
                    sg.Popup('oops! Je moet de locaties nog kiezen')
                    continue

                if values['moordenaar1'] == '':
                    event = 'Error'
                    values['exception'] = 'moordenaar1'
                    sg.Popup('oops! Je moet moordenaar 1 nog kiezen')
                    continue

                if values['moordenaar2'] == '':
                    event = 'Error'
                    values['exception'] = 'moordenaar2'
                    sg.Popup('oops! Je moet moordenaar 2 nog kiezen')
                    continue

                if values['moordenaar1'] == values['moordenaar2']:
                    event = 'Error'
                    values['exception'] = 'verschillende'
                    sg.Popup('oops! Je moet verschillende moordenaars kiezen!')
                    continue

                correct_weapon = values['weapons'] in list(df_murder['items'])
                correct_location = values['locations'] in list(df_murder['items'])
                correct_moordenaar1 = values['moordenaar1'] in list(df_murder['items'])
                correct_moordenaar2 = values['moordenaar2'] in list(df_murder['items'])
                if correct_weapon & correct_location & correct_moordenaar1 & correct_moordenaar2:
                    sg.Popup('Helemaal correct! Je hebt de moord gepleegd of voorkomen!')
                else:
                    sg.Popup('Helaas, één of meerdere van je keuzes waren incorrect. Je mag in dit spel niet nogmaals raden.')



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

values =  gui_input()