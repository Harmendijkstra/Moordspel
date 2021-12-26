import email
import smtplib
import create_GUI
import pandas as pd
from random import randrange
import random
from pathlib import Path
import numpy as np
from fpdf import FPDF

weapons_options = ['lepel', 'vork', 'mes', 'pen', 'boek', 'pan',
             'sleutel', 'kussen', 'kleerhanger', 'jas',
             'potlood', 'schaar', 'schilmesje', 'schoen',
             'beker', 'bezem', 'handdoek', 'zeep', 'beeldje',
             'klok', 'touw', 'washand', 'corona sneltest', 'vies koekje']
locations_options = ['tuin', 'woonkamer', 'keuken', 'gang',
             'studeer', 'zolder', 'badkamer', 'overloop', 
             'voor het huis', 'slaapkamer 1', 'slaapkamer 2',
             'slaapkamer 3', 'slaapkamer 4', 'wc', 'bijkeuken']



gui_input = create_GUI.gui_input()
if (gui_input['event'] == 'Submit') and (gui_input['exception'] == 'None'):
    emails_all = gui_input['emails'].split('\n')
    emails = list(filter(None, emails_all)) 
    locations = gui_input['locations']
    weapons = gui_input['weapons']
    nr_killers = int(gui_input['nr_killers'])
    knowledge = gui_input['knowledge']
    knowledge_people = gui_input['knowledge_people']

def choose_the_murder(emails, locations, weapons, nr_killers):
    murder = {'emails': '', 'location': '', 'weapon': ''}
    killers = []
    remaining_emails = emails
    for nr_killer in range(nr_killers):
        random_email = remaining_emails[randrange(len(remaining_emails))]
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

#TODO enters in mail stoppen!
def send_murder_emails(murder, murder_itemlist, weapons, emails, locations, murder_emails):
    for email_adress in murder['emails']:
        extra_info = murder_itemlist[0]
        extra_info_str = ', '.join(extra_info)
        del murder_itemlist[0]
        message = f'Gegroet inwoner van Loppersum, \
\n \n \
Jij bent een moordenaar! Zoek het wapen, je mede moordenaars \
(er zijn in totaal {nr_killers} moordenaars) en de locatie zodat je de \
moord kan plegen! Wat jij verder nog weet, is dat de moord niet gepleegd wordt in/met/door: \n \
{extra_info_str}. \
\n \
Dit zijn alle wapens: \n \
{weapons} \n \
Dit zijn alle locaties: \n \
{locations} \n \
Dit zijn alle emails: \n \
{emails}. '
        if knowledge == 'Ja':
            murder_emails_str = ', '.join(murder_emails)
            knowledge_info = f'Als moordenaar weet jij nog iets meer, namelijk alle moordenaars. Dit zijn alle moordenaars: {murder_emails_str}'
            message = message + knowledge_info
        send_email(email_adress, message)
        
def send_detective_emails(remaining_items, other_itemlist, weapons, emails, locations, other_emails):
    for email_ad in other_emails:
        print(email_ad)
        extra_info = other_itemlist[0]
        extra_info_str = ', '.join(extra_info)
        del other_itemlist[0]
        message = f'Gegroet inwoner van Loppersum, \
\n \n \
Jij bent geen moordenaar, zoek de {nr_killers} moordenaars in Loppersum! \
Verder moet je het wapen en de locatie weten om zo de moord te stoppen! \
Wat jij verder nog weet, is dat de moord niet gepleegd wordt in/met/door: \n \
{extra_info_str}. \
\n \
Dit zijn alle wapens: \n \
{weapons} \n \
Dit zijn alle locaties: \n \
{locations} \n \
Dit zijn alle emails: \n \
{emails}.'
        send_email(email_ad, message)

def flatten(full_list):
    return sum(full_list, [])

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        
def shuffle_remaining_items(list_to_shuffle):
    random.shuffle(list_to_shuffle)
    return list(chunks(list_to_shuffle, 3))

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

def extract_murder(murder_emails, murder_weapon, murder_location):
    df_murder = pd.DataFrame(columns = ['items'])
    for row in range(len(murder_emails)):
        df_murder.loc[row, 'items'] = murder_emails[row]
    #TODO just fast fix, redo later!
    row = row + 1
    df_murder.loc[row, 'items'] = murder_weapon
    row = row + 1
    df_murder.loc[row, 'items'] = murder_location
    df_murder
    return df_murder

def save_murder(df_murder):
    df_emails = pd.DataFrame(emails)
    df_weapons = pd.DataFrame(weapons)
    df_locations = pd.DataFrame(locations)

    parent_dir = 'Secret/'
    Path(parent_dir).mkdir(parents=True, exist_ok=True)
    filepath = parent_dir +'/Secretinfo.xlsx'

    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
    df_murder.to_excel(writer, sheet_name='Murder')
    df_emails.to_excel(writer, sheet_name='Emails')
    df_weapons.to_excel(writer, sheet_name='Weapons')
    df_locations.to_excel(writer, sheet_name='Locations')
    writer.save()


def create_murder_list(remaining_items):
    random_nrs = random.sample(range(0, len(remaining_items['emails'])), int(knowledge_people))
    non_murders = np.array(remaining_items['emails'])
    persons_for_murders = list(non_murders[random_nrs])
    remaining_emails = list(set(remaining_items['emails']) - set(persons_for_murders))
    remaining_items['emails'] = remaining_emails
    nr_other_items = (nr_killers*3) - int(knowledge_people)
    all_items = flatten(list(remaining_items.values()))

    random_nrs_rest = random.sample(range(0, len(all_items)), nr_other_items)
    rest_items = np.array(all_items)
    restitems_for_murders = list(rest_items[random_nrs_rest])
    murder_itemlist = restitems_for_murders + persons_for_murders
    other_itemlist = list(set(flatten(list(remaining_items.values()))) - set(murder_itemlist))
    return murder_itemlist, other_itemlist

murder, remaining_items = choose_the_murder(emails, locations, weapons, nr_killers)
other_emails = list(set(emails) - set(murder['emails']))
murder_emails = murder['emails']
murder_weapon = murder['weapon']
murder_location = murder['location']

murder_itemlist, other_itemlist = create_murder_list(remaining_items)

other_itemlist = shuffle_remaining_items(other_itemlist)
murder_itemlist = shuffle_remaining_items(murder_itemlist)
emails_str = ', '.join(emails)
locations_str = ', '.join(locations)
weapons_str = ', '.join(weapons)
send_murder_emails(murder, murder_itemlist, weapons_str, emails_str, locations_str, murder_emails)
send_detective_emails(remaining_items, other_itemlist, weapons_str, emails_str, locations_str, other_emails)
send_murder_info(murder)
df_murder = extract_murder(murder_emails, murder_weapon, murder_location)
save_murder(df_murder)


def save_image(image_text):
    image_dir = 'Images/'
    image_path = image_dir + image_text + '.pdf'
    Path(image_dir).mkdir(parents=True, exist_ok=True)
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font('Courier','B',16)
    pdf.cell(40,10, image_text)
    pdf.output(image_path,'F')