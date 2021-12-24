import email
import smtplib
import create_GUI
import pandas as pd
from random import randrange
import random


gui_input = create_GUI.gui_input()
if (gui_input['event'] == 'Submit') and (gui_input['exception'] == 'None'):
    emails_all = gui_input['emails'].split('\n')
    emails = list(filter(None, emails_all)) 
    locations = gui_input['locations']
    weapons = gui_input['weapons']
    nr_killers = int(gui_input['nr_killers'])

def choose_the_murder(emails, locations, weapons, nr_killers):
    murder = {'emails': '', 'location': '', 'weapon': ''}
    killers = []
    remaining_emails = emails
    for nr_killer in range(nr_killers):
        random_email = emails[randrange(len(emails))]
        remaining_emails = list(set(remaining_emails) - set([random_email]))
        killers.append(random_email)
    random_location = locations[randrange(len(locations))]
    random_weapon = weapons[randrange(len(weapons))]
    remaining_weapons = list(set(weapons) - set([random_weapon]))
    remaining_locations = list(set(locations) - set([random_location]))
    murder['emails'] = killers
    murder['location'] = random_location
    murder['weapon'] = random_weapon
    
    remaining_items = {'emails': '', 'locations': '', 'weapons': ''}
    remaining_items['emails'] = remaining_emails
    remaining_items['locations'] = remaining_locations
    remaining_items['weapons'] = remaining_weapons
    return murder, remaining_items

def send_murder_emails(murder, item_list, weapons, emails, locations):
    for email_adress in murder['emails']:
        extra_info = item_list[0]
        extra_info_str = ', '.join(extra_info)
        del item_list[0]
        message = f'Gegroet inwoner van Loppersum, \
\n \n \
Jij bent een moordenaar! Zoek het wapen, je mede moordenaars \
(er zijn in totaal {nr_killers} moordenaars) en de locatie zodat je de \
moord kan plegen! Wat jij verder nog weet is dat de moord niet gepleegd word in/met/door: {extra_info_str}. \
Dit zijn alle wapens: {weapons}, dit zijn alle locaties: {locations},  dit zijn alle emails: {emails}.'
        send_email(email_adress, message)
        
def send_detective_emails(remaining_items, item_list, weapons, emails, locations):
    for email_adress in remaining_items['emails']:
        extra_info = item_list[0]
        extra_info_str = ', '.join(extra_info)
        del item_list[0]
        message = f'Gegroet inwoner van Loppersum, \
\n \n \
Jij bent geen moordenaar, zoek de {nr_killers} moordenaars in Loppersum! \
Verder moet je het wapen en de locatie weten om zo de moord te stoppen! \
Wat jij verder nog weet is dat de moord niet gepleegd word in/met/door: {extra_info_str}. \
Dit zijn alle wapens: {weapons}, dit zijn alle locaties: {locations},  dit zijn alle emails: {emails}.'
        send_email(email_adress, message)

def flatten(full_list):
    return sum(full_list, [])

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        
def shuffle_remaining_items(remaining_items):
    all_items = flatten(list(remaining_items.values()))
    random.shuffle(all_items)
    return list(chunks(all_items, 3))


def send_email(email_adress, message, subject_info=''):
    msg = email.message_from_string(message)
    msg['From'] = "Moordspelinloppersum@hotmail.com"
    msg['To'] = email_adress
    if subject_info == '':
        msg['Subject'] = "Ben jij een moordenaar?"
    else:
        msg['Subject'] = subject_info
        
    
    s = smtplib.SMTP("smtp.live.com",587)
    s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    s.starttls() #Puts connection to SMTP server in TLS mode
    s.ehlo()
    s.login('Moordspelinloppersum@hotmail.com', 'Wieisdedader?')
    
    s.sendmail("Moordspelinloppersum@hotmail.com", email_adress, msg.as_string())
    
    s.quit()

def send_murder_info(murder):
    email_message = f'Gegroet inwoner van Loppersum, \
\n \n \
Weet jij de plannen voor de moord? De plannen zijn: {murder}'
    subject_info = 'Ultra geheim, dit zijn de plannen voor de moord!'
    send_email('Moordspelinloppersum@hotmail.com', email_message, subject_info)

murder, remaining_items = choose_the_murder(emails, locations, weapons, nr_killers)
item_list = shuffle_remaining_items(remaining_items)
emails_str = ', '.join(emails)
locations_str = ', '.join(locations)
weapons_str = ', '.join(weapons)
send_murder_emails(murder, item_list, weapons_str, emails_str, locations_str)
send_detective_emails(remaining_items, item_list, weapons_str, emails_str, locations_str)
send_murder_info(murder)

if len(item_list) != 0:
    send_email('harmen_dijkstra@hotmail.com', 'There was an error, still some items not picked')

