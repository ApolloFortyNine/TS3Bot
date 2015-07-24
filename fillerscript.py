import time
from filler import Filler
import config
from ts3 import TS3Server
import datetime

# Outer loop running through all challenger teams (dataM)
def fill_database():
    filler = Filler()
    start = time.time()

    server = TS3Server(config.serveraddress, 10011, 1)
    server.login(config.username, config.password)
    server.send_command('use', keys={'port': 9987})

    allClients = server.clientlist()
    clientList = []

    channels = server.send_command('channellist').data

    for x in channels:
        if x['channel_name'] == 'AFK':
            afkcid = x['cid']

    for x in allClients:
        if (int(allClients[x]['client_type']) == 0) & (str(allClients[x]['cid']) != str(afkcid)):
            clientList.append(allClients[x])
            continue

    for x in clientList:
        x['username'] = x['client_nickname']
        x['clientDatabaseId'] = x['client_database_id']
        x['startTime'] = datetime.datetime.now()
        x['endTime'] = datetime.datetime.now()
        x['totalTime'] = 0
        x['idleTime'] = 0
        x['online'] = True

        x.pop("cid", None)
        x.pop("client_type", None)
        x.pop("client_nickname", None)
        x.pop("client_database_id", None)

    filler.add_all_users(clientList, server, afkcid)


    print(time.time() - start)

fill_database()