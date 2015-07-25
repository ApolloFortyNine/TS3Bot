from database import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *


class Filler:
    def __init__(self):
        self.engine = create_engine("sqlite:///users.db")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.warning_afk = 1800 * 1000
        self.marked_afk = 2700 * 1000
        Base.metadata.create_all(self.engine, checkfirst=True)

    def add_all_users(self, allusers, server, afkid):
        online_users = self.usersOnline = self.session.query(UserInfo).filter(
            UserInfo.online == True).all()

        clients = []
        clientIds = []
        for x in allusers:
            if str(x['clientDatabaseId']) not in clientIds:
                clients.append(x)
                clientIds.append(x['clientDatabaseId'])
        client_infos = {}
        user = {}
        print(clients)
        for x in online_users:
            if str(x.clientDatabaseId) in clientIds:
                for y in clients:
                    if x.username == y['username']:
                        user = y
                        if server.send_command('clientinfo',
                                                             keys={'clid': user['clid']}).is_successful:
                            client_infos[user['clid']
                                     ] = server.send_command('clientinfo',
                                                             keys={'clid': user['clid']}).data
                        break
                x.endTime = datetime.datetime.now()
                x.totalTime = (x.endTime - x.startTime).total_seconds()
                client_info = client_infos[user['clid']]
                x.idleTime = int(client_info[0]['client_idle_time'])
                #if x.idleTime >= self.marked_afk:
                #    x.online = False
                #    x.endTime = x.endTime - datetime.timedelta(minutes=15)
                #    x.idleTime = x.idleTime - (15 * 60)
                if (int(client_info[0]['client_idle_time']) >= self.warning_afk) and (user['messege_sent'] == False):
                    server.send_command('sendtextmessage', keys={'targetmode': 1, 'target': user['clid'], 'msg':
                        'If you are not afk, respond to this messege. You will be marked afk in 15 minutes.'})
                    user['messege_sent'] == True
                elif (int(client_info[0]['client_idle_time']) >= self.marked_afk) and (user['messege_sent'] == True):
                    server.send_command('clientmove', keys={'clid': user['clid'], 'cid': afkid})
                    user['online'] = False
                for y in clients:
                    if y['clientDatabaseId'] == str(x.clientDatabaseId):
                        clients.remove(y)
                        break
            else:
                x.online = False

        print(clients)

        for x in clients:
            if x['clid'] in client_infos.keys():
                client_info = client_infos[x['clid']]
            else:
                if server.send_command('clientinfo', keys={'clid': x['clid']}).is_successful:
                    client_info = server.send_command('clientinfo', keys={'clid': x['clid']}).data
            if (int(client_info[0]['client_idle_time']) >= self.warning_afk) and (x['messege_sent'] == False):
                server.send_command('sendtextmessage', keys={'targetmode': 1, 'target': x['clid'], 'msg':
                    'If you are not afk, respond to this messege. You will be marked afk in 15 minutes.'})
                x['messege_sent'] == True
            x.pop('clid', None)
            x.pop('messege_sent', None)
            self.session.add(UserInfo(**x))
        self.session.commit()
