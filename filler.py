from database import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *


class Filler:
    def __init__(self):
        self.engine = create_engine("sqlite:///users.db")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine, checkfirst=True)

    def add_all_users(self, allusers):
        online_users = self.usersOnline = self.session.query(UserInfo).\
            filter(UserInfo.online == True).all()

        clientIds = []
        for x in allusers:
            clientIds.append(allusers[x])

        print(clientIds)

        for x in online_users:
            if x.clientDatabaseId in clientIds:
                x.endTime = datetime.now()
                x.totalTime = (x.endTime - x.startTime).inSeconds()
                clientIds.remove(x)
            else:
                x.online = False

        for x in clientIds:
            print(type(x))
            self.session.add(UserInfo(**x))
        self.session.commit()
