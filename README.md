# TS3Bot

To connect to teamspeak through telnet and use commands do:
login NAME PASSWORD
use port=9987
clientlist
clientinfo clid=VALUE

# Dataflow

* Create a filler class.
* Call a function inside the filler class, passing the dictionary of online users.
* Grab all current online users from DB
* Check online users in DB with actual online users
* If already online, update end time. If not, create new row for user
* Make sure to update time idle column, and check if speakers are muted

# Formatter

Install yapf (pip install yapf), then inside project directory run "yapf --style yapf.config -i ."