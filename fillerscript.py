import time
from filler import Filler
import config
from ts3 import TS3Server

# Outer loop running through all challenger teams (dataM)
def fill_database():
    filler = Filler()
    start = time.time()

    server = TS3Server(config.serveraddress, 10011, 1)
    server.login(config.username, config.password)
    server.send_command('use', keys={'port': 9987})

    clientList = server.clientlist()
    filler.add_all_users(clientList)


    print(time.time() - start)

fill_database()