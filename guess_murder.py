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
att_sign = '@'
which_are_murders = [att_sign in item for item in  df_murder['items']]
nr_of_murders = sum(which_are_murders)

def gui_input():
    sg.ChangeLookAndFeel('DarkAmber')

    murder_block = []
    for murd in range(1, nr_of_murders+1):
        murder_block.append([sg.Text(f'Kies moordenaar {murd} (volgorde moordenaar maakt niet uit, kies wel verschillende):')])
        murder_block.append([sg.Combo(emails, size=(20, len(emails)), key=f'moordenaar{murd}')])

    layout = [
        [sg.Text('Kies moordwapen:')],
        [sg.Combo(weapons, size=(20, len(weapons)), key='weapons')],

        [sg.Text('Kies locatie:')],
        [sg.Combo(locations, size=(20, len(locations)), key='locations')],
        
        murder_block,

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

                if '' in list(values.values()):
                    event = 'Error'
                    values['exception'] = 'moordenaar ont'
                    sg.Popup('oops! Je moet alle moordenaars invullen!')
                    continue

                all_values = list(values.values())
                if (len(set(all_values)) != len(all_values)):
                    event = 'Error'
                    values['exception'] = 'verschillende'
                    sg.Popup('oops! Je moet verschillende moordenaars kiezen!')
                    continue

                correct_murder = list(df_murder['items'])
                exclude_keys = ['event', 'exception']
                guessed_murder = {k: values[k] for k in set(list(values.keys())) - set(exclude_keys)}
                guessed_murder_list = list(guessed_murder.values())
                if set(guessed_murder_list) == set(correct_murder):
                    sg.Popup('Helemaal correct! Je hebt de moord opgelost of je bent ontsnapt!')
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