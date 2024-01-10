from telethon import TelegramClient, types, sync, events
#from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
import re
import pytz

# Вставляем api_id и api_hash
api_id = ...
api_hash = '...'
client = TelegramClient('telegramOsint', api_id, api_hash)
#For two-factor authorization
#client.start(password="Qwerty123")
client.start()

def get_telegram_contact_info(contact_phone_number):
    try:
        contact = InputPhoneContact(client_id=92, phone=contact_phone_number, first_name="", last_name="")
        result = client(ImportContactsRequest([contact]))
        res = []
        contact_info = client.get_entity(contact_phone_number)
        res.append(contact_info.phone)
        res.append(contact_info.id)
        res.append(contact_info.username)
        res.append(contact_info.first_name)
        res.append(contact_info.last_name)
        res.append(client.download_profile_photo(contact_info.id))
        try:
            res.append(contact_info.status.was_online.astimezone(pytz.timezone('Europe/Kiev')))
        except:
            res.append("None")
        return res
    except Exception as err:
        print(err)
        print('Cannot find any entity corresponding to "{}"'.format(contact_phone_number))
        pass
while True:
    contact_phone_number = str(input("Enter number or 'q' to exit: "))
    if contact_phone_number == 'q': exit()
    elif re.match(r"^((8|\+\d{1})[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", contact_phone_number) == None:
        print("wrong number, re-enter")
        continue
    try:
        print("Number\tID\tUsername\tFirst_name\tLast_name\tPhoto\tLast_Online")
        print('\t'.join(str(x) for x in get_telegram_contact_info(contact_phone_number)))
    except Exception as err:
        print(err)
        print ('net telegi ili skrit nastrojkami privatnosti')
