import os, sys, re
import time, threading
import json
import feedparser
import logging
from datetime import datetime
from time import mktime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import exc

from models import FeedItem, Feed

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(filename=os.getenv('LOG_FILE'), 
                    level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s :: %(levelname)-8s :: %(message)s')
log = logging.getLogger(__name__)


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


class NewsParser():
    rss_feeds_file = os.getenv('__PROJECT__') + os.getenv('RSS_FEEDS_JSON')
    engine = create_engine(os.getenv('DB_URL'))
    Session = sessionmaker(bind=engine)
    db = Session()
    
    def update_from_json(self):
        with open(self.rss_feeds_file) as json_file:
            feeds_arr = json.load(json_file)
        
        for feed in feeds_arr:
            f = Feed()
            f.url = feed['url']
            f.website_url = feed['website_url']
            f.website_name= feed['website_name']
            
            try:
                self.db.add(f)
                self.db.commit()
            except exc.IntegrityError:
                self.db.rollback()
                log.warning(f'==RSS feed already exists "{f.url}"')
    
    def get_feeds(self):
        self.update_from_json()
        return self.db.query(Feed)
                
    def get_attr(self, entry, name):
        if name in entry:
            return entry[name]

    def get_feed_item(self, url):
        return self.db.query(FeedItem).filter_by(url=url)

    def run(self):
        feeds = self.get_feeds()
        for feed in feeds:
            # "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
            fpd = feedparser.parse(feed.url)
            
            for entry in fpd.entries:
                url = self.get_attr(entry, 'link')
                existing_feed = self.get_feed_item(url).first()
                
                if existing_feed:
                    log.warning(f'FeedItem already exists "{url}"')
                else:
                    fi = FeedItem()
                    fi.title = self.get_attr(entry, 'title')
                    fi.url = url
                    fi.author = self.get_attr(entry, 'author')
                    fi.tags = self.get_attr(entry, 'tags')
                    fi.summary = cleanhtml(self.get_attr(entry, 'summary'))
                    
                    content = self.get_attr(entry, 'content')
                    if content:
                        fi.content = cleanhtml(content[0].value)
                    else:
                        log.info('no content in this entry')
                    
                    stime = self.get_attr(entry, 'published_parsed')
                    
                    fi.pub_date = datetime.fromtimestamp(mktime(stime))
                    fi.epoch = int(time.time())
                    fi.feed_id = feed.id
                                
                    self.db.add(fi)
                    self.db.commit()
                    log.info('==Feed item added :)')
                    
        log.info('== get_news finished...')
    

parser = NewsParser()
    
def run_forever():
    parser.run()
    threading.Timer(60*5, run_forever).start()

if __name__ == '__main__':
    log.info('== get_news started...')
    if sys.argv and sys.argv[0] == 'prd':
        run_forever()
    else:
        parser.run()
