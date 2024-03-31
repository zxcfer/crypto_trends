# importing all required libraries
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
 
  
# get your api_id, api_hash, token
# from telegram as described above

class Notifier:
    
    def send_telegram(self, to, msg):
        api_id = 'API_id'
        api_hash = 'API_hash'
        token = 'bot token'
        message = "Working..."
         
        phone = 'YOUR_PHONE_NUMBER_WTH_COUNTRY_CODE'
        client = TelegramClient('session', api_id, api_hash)
        client.connect()
         
        # in case of script ran first time it will
        # ask either to input token or otp sent to
        # number or sent or your telegram id
        if not client.is_user_authorized():
            client.send_code_request(phone)
             
            # signing in the client
            client.sign_in(phone, input('Enter the code: '))
          
        try:
            # receiver user_id and access_hash, use
            # my user_id and access_hash for reference
            receiver = InputPeerUser('user_id', 'user_hash')
            client.send_message(receiver, message, parse_mode='html')
        except Exception as e:
            print(e);
        client.disconnect()
        
    
    def send_mail(self, email, msg):
        subj = 'Alert 21 happened'
        pass
    
    
    def tweet(self, username, msg):
        pass