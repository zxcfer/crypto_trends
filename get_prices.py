# -*- coding: utf-8 -*-
import logging
import os
import sys
import threading
import csv
import math
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from pycoingecko import CoinGeckoAPI
from models import Price
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename=os.getenv('LOG_FILE'), 
                    level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s :: %(levelname)-8s :: %(message)s')
log = logging.getLogger(__name__)

# https://www.coingecko.com/es/api/documentation

# TODO: get date, hour, min 
# TODO: save day price from: https://api.coingecko.com/api/v3/coins/bitcoin/history?date=21-03-2022&localization=es
#
# {"id":"bitcoin",
# "symbol":"btc",
# "name":"Bitcoin",
# "localization":{"en":"Bitcoin","sl":"Bitcoin"},
# "image":{"thumb":"https://assets.coingecko.com/coins/images/1/thumb/bitcoin.png?1547033579",
# "small":"https://assets.coingecko.com/coins/images/1/small/bitcoin.png?1547033579"},
# "market_data":{"current_price":{"aed":151634.2772592798,"usd":41283.25900104565,"bits":1000072.4604869285,"link":2836.8184864321856,"sats":100007246.04869285},
# "market_cap":{"aed":2879848514617.3813,"usd":784054464871.6631,"vef":78507373567.59966,"sats":1899414891234072.5},
# "total_volume":{"aed":61913148305.13767,
# "sats":40833534264906.36}},
# "community_data":{"facebook_likes":null,
# "twitter_followers":4855461,
# "reddit_average_posts_48h":7.3,
# "reddit_average_comments_48h":633.5,
# "reddit_subscribers":4019848,
# "reddit_accounts_active_48h":"1382.81818181818"},
# "developer_data":{"forks":31873,
# "stars":62633,
# "subscribers":3903,
# "total_issues":6786,
# "closed_issues":6177,
# "pull_requests_merged":9536,
# "pull_request_contributors":772,
# "code_additions_deletions_4_weeks":{"additions":108788,
# "deletions":-110272},
# "commit_count_4_weeks":238},
# "public_interest_stats":{"alexa_rank":7863,
# "bing_matches":null}}

# TODO: do not delete hour price nor day price when clean database
# TODO: get coingecko ID : http -h --download https://api.coingecko.com/api/v3/coins/list 

def generate_csv_name():
    now = datetime.now()
    first_part = now.strftime('%Y%m%d')
    last_part = 5 * math.floor(int(now.strftime('%H%M'))/5)
    return f"crypto_{ first_part}_{last_part:04d}.csv"


class CoinPriceUpdater:
    engine = create_engine(os.getenv('DB_URL'))
    Session = sessionmaker(bind=engine)
    db = Session()
    cg = CoinGeckoAPI()
    
    PROJECT_DIR = os.getenv('__PROJECT__')
    
    date = datetime.now()
    
    def generate_csv(self):
        sql = text("""
        select cp.coin, cp.price_btc, cp.created_at from coin_prices cp
         where cp.created_at between DATE_SUB(NOW(), INTERVAL 9 MINUTE) 
                                 and NOW();
        """)
        coin_prices = self.db.execute(sql)

        csv_filename = generate_csv_name()
        with open(f"/tmp/{csv_filename}", 'a+') as csv_file:
            line_writer = csv.writer(csv_file)
            line_writer.writerow(['crypto','price','pulled_at'])
            for coin in coin_prices:
                line_writer.writerow(coin)
            

    def run(self):
        coins = self.cg.get_coins_markets(order='market_cap_desc',
                                          vs_currency='btc',
                                          per_page=100,
                                          page=1)

        coins_usd = self.cg.get_coins_markets(order='market_cap_desc',
                                              vs_currency='usd',
                                              per_page=100,
                                              page=1)

        for i, coin in enumerate(coins):
            cp = Price()
            cp.symbol = coin['symbol']
            cp.price_btc = coin['current_price']
            if coin['symbol'] == coins_usd[i]['symbol']:
                cp.price_usd = coins_usd[i]['current_price']
                cp.market_cap = coins_usd[i]['market_cap']
            cp.utcdate = self.date.date()
            cp.hour = self.date.hour
            cp.minu = self.date.minute
            self.db.add(cp)
    
        self.db.commit()
        log.info('== get_prices finished...')
        
        # self.generate_csv()
        # log.info('== CSV file generated...')

cpu = CoinPriceUpdater()


def run_forever():
    log.info('executed :)')
    cpu.run()
    threading.Timer(10*60, run_forever).start()


if __name__ == '__main__':
    log.info('== get_prices started...')
    if sys.argv and sys.argv[0] == 'PRD':
        run_forever()
    else:
        cpu.run()
