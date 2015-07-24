from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class UserInfo(Base):
    __tablename__ = 'user_info'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)
    username = Column(String)
    clientDatabaseId = Column(Integer)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    totalTime = Column(BigInteger)
    online = Column(Boolean)
