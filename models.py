# from sqlalchemy import ForeignKey
from sqlalchemy import Column, DateTime, String, Integer, func, Numeric, Date  
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Price(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(255))
    price_usd = Column(Numeric(20,8))
    price_btc = Column(Numeric(20,8))
    market_cap = Column(Numeric(20,8))
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    utcdate = Column(Date, nullable=False)
    hour = Column(Integer, default=0)
    minu = Column(Integer, default=0)

    @classmethod    
    def current(cls, session, coin, date, hour, minute):
        return session.query(cls).filter(cls.symbol==coin,
                                         cls.date==date,
                                         cls.hour==hour,
                                         cls.min==minute)

    @classmethod    
    def last(cls, session, coin, lapse_type, lapse):
        return session.query(cls).filter(cls.symbol==coin, cls.typ==lapse_type).limit(lapse)


class Coin(Base):
    __tablename__ = 'coins'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(255))
    marketcap = Column(Numeric(20,2))
    
    epoch = Column(Integer)


class MarketPlace(Base):
    __tablename__ = 'market_place'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    created_at = Column(DateTime(), default=func.now())
   

class Alert(Base):
    __tablename__ = 'user_alerts'

    DISABLED = 0
    ENABLED = 1
    
    LOWEST = 0
    HIGHEST = 1
         
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255))
    alert_type = Column(Numeric(20,2))
    crypto = Column(Numeric(20,2))
    reference = Column(Numeric(20,2))
    threshold = Column(Numeric(20,2))
    direction = Column(Numeric(20,2))
    status = Column(Numeric(20,2))
    channels = Column(Numeric(20,2))
    
    created_at = Column(DateTime(), default=func.now())
    epoch = Column(Integer)

    @classmethod
    def active(cls, domain, limit=20):
        items = cls.objects.filter(cls.status==1)
        return items

    def disable(self, session):
        self.status = Alert.DISABLED
        session.commit()
    
class UserChannel(Base):
    __tablename__ = 'user_channels'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255))
    channel_type = Column(Numeric(20,2))
    status = Column(Numeric(20,2))
    
    created_at = Column(DateTime(), default=func.now())
    epoch = Column(Integer)
    
    @classmethod
    def by_user(cls, user):
        items = cls.objects.filter(cls.user==user)
        return items



class UserAlert(Base):
    __tablename__ = ''

    id = Column(Integer, primary_key=True)
    alert_id = Column(Integer)
    channels = Column(Integer)
    msg = Column(String(190), nullable=False)
    
    created_at = Column(DateTime(), default=func.now())
    epoch = Column(Integer)

    @classmethod
    def active(cls, domain, limit=20):
        items = cls.objects.filter(status=1)
        return items


class AlertType(Base):
    __tablename__ = 'alert_types'

    id = Column(Integer, primary_key=True)
    coin = Column(String(255))
    marketcap = Column(Numeric(20,2))
    
    created_at = Column(DateTime(), default=func.now())
    epoch = Column(Integer)

    