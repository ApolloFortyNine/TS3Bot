import time
from filler import Filler
from config import Config
from ts3 import TS3Server

# Outer loop running through all challenger teams (dataM)
def fill_database():
    filler = Filler()
    start = time.time()

    c = Config()
    server = TS3Server(c.serveraddress, 10011, 1)
    server.login(c.username, c.password)
    server.send_command('use', keys={'port': 9987})

    clientList = server.clientlist()
    filler.add_all_users(clientList)


    print(time.time() - start)

fill_database()