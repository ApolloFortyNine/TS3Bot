from database import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *


class Filler:
    def __init__(self):
        self.engine = create_engine("sqlite:///users.db")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine, checkfirst=True)

    def add_all_users(self, allusers, server, afkid):
        online_users = self.usersOnline = self.session.query(UserInfo).filter(UserInfo.online ==
                                                                              True).all()

        clients = []
        clientIds = []
        for x in allusers:
            if str(x['clientDatabaseId']) not in clientIds:
                clients.append(x)
                clientIds.append(x['clientDatabaseId'])
        client_infos = {}
        user = {}
        for x in online_users:
            if str(x.clientDatabaseId) in clientIds:
                for y in clients:
                    if x.username == y['username']:
                        user = y
                        client_infos[user['clid']] = server.send_command('clientinfo', keys={'clid': user['clid']}).data
                        break
                x.endTime = datetime.datetime.now()
                x.totalTime = (x.endTime - x.startTime).total_seconds()
                client_info = client_infos[user['clid']]
                x.idleTime = int(client_info[0]['client_idle_time'])
                if x.idleTime >= 900000:
                    x.online = False
                    #server.send_command('clientmove', keys={'clid': user['clid'], 'cid': afkid})
                    x.endTime = x.endTime - datetime.timedelta(minutes=15)
                    x.idleTime = x.idleTime - (15*60)
                for y in clients:
                    if y['clientDatabaseId'] == str(x.clientDatabaseId):
                        clients.remove(y)
                        break
            else:
                x.online = False

        for x in clients:
            if x['clid'] in client_infos.keys():
                print('hi')
                client_info = client_infos[x['clid']]
            else:
                client_info = server.send_command('clientinfo', keys={'clid': x['clid']}).data
            if int(client_info[0]['client_idle_time']) >= 900000:
                x['online'] = False
            x.pop('clid', None)
            self.session.add(UserInfo(**x))
        self.session.commit()
