# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
import threading
from datetime import timedelta
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.sql import and_
from pycoingecko import CoinGeckoAPI
from models import CryptoPrice
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename=os.getenv('LOG_FILE'), 
                    level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s :: %(levelname)-8s :: %(message)s')
log = logging.getLogger(__name__)


class CoinPriceUpdater:
    engine = create_engine(os.getenv('DB_URL'))
    Session = sessionmaker(bind=engine)
    db = Session()

    PROJECT_DIR = os.getenv('__PROJECT__')

    def gen_last(self):
        now = datetime.now()
        now_1hr = datetime.now()-timedelta(hours=1)
        query = self.db.query(
        ).group_by(CryptoPrice.name).all()

    def run(self):
        coins = self.cg.get_coins_markets(order='market_cap_desc',
                                          vs_currency='usd',
                                          per_page=100,
                                          page=1)
        for coin in coins:
            cp = CryptoPrice()
            cp.coin = coin['symbol']
            cp.price = coin['current_price']
            cp.epoch = int(time.time())
            self.db.add(cp)
    
        self.db.commit()
        
        log.info('== get_prices finished...')

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
