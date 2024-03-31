import os
import logging
from datetime import datetime
from util import is_min, is_max
from models import Alert, UserAlert, Price, UserChannel
from notifier import Notifier
# This script runs every minute at second 30 (re-run 3 times if data not present)


logging.basicConfig(filename=os.getenv('LOG_FILE'), 
                    level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s :: %(levelname)-8s :: %(message)s')
log = logging.getLogger(__name__)

# -- add dir, update according > or < in price alert
#             update when percent is + or -
#              0 if that momement is more than alert
#              1 if that momemtn alert is less
# /alert del(ete) remove :ID

now = datetime.now()
current_date = now.date() 
current_hour = now.hour
current_min = now.minute 

def notify(ua):
    user_channels = UserChannel.by_user(ua.user)
    for uc in user_channels: 
        if uc.typ == 'TELEGRAM':
            Notifier.send_telegram(uc.username, ua.msg)

        # if uc.typ == 'SMS':
        #     Notifier.send_sms(uc.username, ua.msg)
            
        if uc.typ == 'EMAIL':
            Notifier.send_mail(uc.username, ua.msg)

        if uc.typ == 'TWITTER':
            Notifier.tweet(uc.username, ua.msg)
    
# 1. get all active alerts
alerts = Alert.active()
for a in alerts:

    # /alert BTC daily 1
    if a.alert_type == 'PRICE':
        current_price = Price.current(a.coin, current_date, current_min, current_hour)
        
        if a.dir == 1:
            if a.price_usd >= current_price:
                msg = f'{a.currency} reached {a.percert} ({a.threshold})'
                ua = UserAlert(msg)
                a.disable()
                
        elif a.dir == 0:
            if a.price_usd <= current_price:
                msg=f'{a.currency} reached {a.percert} ({a.threshold})'
                ua = UserAlert(msg)
                a.disable()
            
    # /alert BTC min 3h 30 or /alert BTC L(ow)(est) 3h 30
    # /alert BTC max 7d 6 or /alert BTC H(igh)(est) 7d 6
    # TODO: validate lapse > 1 (h or d) msg: lapse should be more than 1.
    elif a.alert_type == 'MAXMIN':
        if a.dir == Alert.LOWEST:
            last_prices = Price.last('eth', a.lapse_type, a.lapse)
            if is_min(a.price_usd, last_prices):
                msg = f'{a.currency} reached the lowest price in {a.lapse} {a.lapse_type} - ${a.price_usd}'

        if a.dir == Alert.HIGHEST:
            last_prices = Price.last('eth', a.lapse_type, a.lapse)
            if is_max(a.price_usd, last_prices):
                msg = f'{a.currency} reached the highest price in {a.lapse} {a.lapse_type} - ${a.price_usd}'
                ua = UserAlert(msg)
                notify(ua)
                

    # /alert ETH D(esc) 5% or /alert ETH -5%
    # /alert btc A(sc) +10% or /alert btc (+)10%
    elif a.alert_type == 'PERCENT':
        if a.dir == 0:
            if a.price_usd <= a.threshold /100:
                ua = UserAlert(msg=f'{a.currency} reached {a.percert} ({a.threshold})')

        if a.dir == 1:
            if a.price_usd >= a.threshold /100:
                ua = UserAlert(msg=f'{a.currency} reached {a.percert} ({a.threshold})')

    # TODO: /alert BTC d(aily) 1 23
    # TODO: /alert BTC h(ourly) 3 30
    elif a.alert_type == 'PERIODIC':
        if a.laptse_type == 'D':
            if current_min == a.offset:
                ua = UserAlert(msg=f'Price of {a.currency} is {a.price}')
            
        elif a.laptse_type == 'H':
            if current_hour == a.offset:
                ua = UserAlert(msg=f'Price of {a.currency} is {a.price}')

        else:
            log.warn('lapse_type not recognized')
