
import pickle
from sendemails import send_email

image_dir = 'Images/'


def read_dict_info():
    parent_dir = 'Secret/'
    with open(parent_dir+'dict_murder.pickle', 'rb') as handle:
        dict_murderemails = pickle.load(handle)
    with open(parent_dir+'dict_detective.pickle', 'rb') as handle:
        dict_detectiveemails = pickle.load(handle)
    return dict_murderemails, dict_detectiveemails



def send_sec_murder_emails(dict_murderemails):
    for email_adress in dict_murderemails:
        extra_info = dict_murderemails[email_adress]['extra_info']
        knowledge = dict_murderemails[email_adress]['knowledge?']
        murder_emails = dict_murderemails[email_adress]['murder_emails']
        nr_killers = dict_murderemails[email_adress]['nr_killers']
        weapons = dict_murderemails[email_adress]['weapons']
        locations = dict_murderemails[email_adress]['locations']
        emails = dict_murderemails[email_adress]['emails']
        info_later = dict_murderemails[email_adress]['info_later?']
        
        extra_info_str= ', '.join(extra_info)
        first_part_mess = f'Gegroet inwoner van Loppersum, \
\n \n \
Jij bent een moordenaar! Al eeder kreeg je een email, maar '
        if info_later:
            specific_mess = f'jij had nog niet alle info gekregen. Vanaf nu heb je extra informatie over de moordenaar(s) \
die je moet laten zien. Je hebt vanaf nu 3 bijlages waar nu ook de extra email(s) tussen staan. \n'
        else:
            specific_mess = f'sommigen hadden nog niet alle informatie gekregen. Er komt vanaf nu extra informatie \
beschikbaar over wie niet de moordenaar(s) zijn. Iedereen heeft daar nu ook bijlages over ontvangen. \
Dus vanaf nu kan je te horen krijgen wie niet de moordenaar(s) zijn! \n'            
        second_part_mess = f'Hier nogmaals alle info: er zijn in totaal {nr_killers} moordenaars en de locatie zodat je de \
moord geheim kan houden! Wat jij verder nog weet, is dat de moord niet gepleegd wordt in/met/door: \n \
{extra_info_str}. \
\n \
Dit zijn alle wapens: \n \
{weapons} \n \
Dit zijn alle locaties: \n \
{locations} \n \
Dit zijn alle emails: \n \
{emails}. '
        message = first_part_mess + specific_mess + second_part_mess
        if knowledge == 'Ja':
            murder_emails_str = ', '.join(murder_emails)
            knowledge_info = f'Als moordenaar weet jij nog iets meer, namelijk alle moordenaars. Dit zijn alle moordenaars: {murder_emails_str}'
            message = message + knowledge_info
        attachments = [image_dir + s + '.pdf' for s in extra_info]
        send_email(email_adress, message, attachments = attachments, subject_info='Mogelijke extra informatie')    
    
    
def send_sec_detective_emails(dict_detectiveemails):
    for email_adress in dict_detectiveemails:
        extra_info = dict_detectiveemails[email_adress]['extra_info']
        nr_killers = dict_detectiveemails[email_adress]['nr_killers']
        weapons = dict_detectiveemails[email_adress]['weapons']
        locations = dict_detectiveemails[email_adress]['locations']
        emails = dict_detectiveemails[email_adress]['emails']
        info_later = dict_detectiveemails[email_adress]['info_later?']
        extra_info_str = ', '.join(extra_info)
        first_part_mess = f'Gegroet inwoner van Loppersum, \
\n \n \
Jij bent geen moordenaar! Al eeder kreeg je een email, maar '
        if info_later:
            specific_mess = f'jij had nog niet alle info gekregen. Vanaf nu heb je extra informatie over de moordenaar(s) \
die je moet laten zien. Je hebt vanaf nu 3 bijlages waar nu ook de extra email(s) tussen staan. \n'
        else:
            specific_mess = f'sommigen hadden nog niet alle informatie gekregen. Er komt vanaf nu extra informatie \
beschikbaar over wie niet de moordenaar(s) zijn. Iedereen heeft daar nu ook bijlages over ontvangen. \
Dus vanaf nu kan je te horen krijgen wie niet de moordenaar(s) zijn! \n'    
        second_part_mess = f'Hier nogmaals alle info: zoek de {nr_killers} moordenaars in Loppersum! \
Verder moet je het wapen en de locatie weten om zo de moordenaars te pakken! \
Wat jij verder nog weet, is dat de moord niet gepleegd is in/met/door: \n \
{extra_info_str}. \
\n \
Dit zijn alle wapens: \n \
{weapons} \n \
Dit zijn alle locaties: \n \
{locations} \n \
Dit zijn alle emails: \n \
{emails}.'
        message = first_part_mess + specific_mess + second_part_mess
        attachments = [image_dir +s + '.pdf' for s in extra_info]
        send_email(email_adress, message, attachments = attachments, subject_info='Mogelijke extra informatie')
    return dict_detectiveemails


dict_murderemails, dict_detectiveemails = read_dict_info()
send_sec_murder_emails(dict_murderemails)
send_sec_detective_emails(dict_detectiveemails)