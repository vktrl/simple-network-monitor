import os, re, time, sys, signal
from datetime import datetime
delay = 1
open('log.txt', 'a').close()

if len(sys.argv) - 1 != 1:
    print("Gib host")
    exit()
else:
    host = str(sys.argv[1])

def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def log(input):
    with open("log.txt", "a") as log:
        message = str(input + "\t" + current_time() + "\n")
        log.write(message)
        print(message)
class connection:
    def __init__(self, host, state):
        self.state = state
    def status(self, state):
        self.state = state
        log("link " + state)
    def ping(self):
        time.sleep(delay)
        response = os.system("ping -c 1 " + host + " 1> /dev/null 2> /dev/null")
        return response
def signal_handler(signal, frame):
  log("Stopped")
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print("Monitoring " + host)
log("---------------------------\nStarted")
link = connection(host, "up")

while True:
    if link.ping() != 0:
        link.status("Dropped")
        while link.ping() != 0:
            time.sleep(1)
        link.status("Restored")