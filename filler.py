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

        clients = []
        clientIds = []
        for x in allusers:
            if str(x['clientDatabaseId']) not in clientIds:
                clients.append(x)
                clientIds.append(x['clientDatabaseId'])


        for x in online_users:
            if str(x.clientDatabaseId) in clientIds:
                x.endTime = datetime.datetime.now()
                x.totalTime = (x.endTime - x.startTime).total_seconds()
                for y in clients:
                    if y['clientDatabaseId'] == str(x.clientDatabaseId):
                        clients.remove(y)
                        break
            else:
                x.online = False

        for x in clients:
            self.session.add(UserInfo(**x))
        self.session.commit()
