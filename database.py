from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class UserInfo(Base):
    __tablename__ = 'user_info'

    timesOnline = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)
    username = Column(String)
    clientDatabaseId = Column(Integer)
    startTime = Column(datetime.datetime)
    endTime = Column(datetime.datetime)
    totalTime = Column(BigInteger)
    online = Column(Boolean)
