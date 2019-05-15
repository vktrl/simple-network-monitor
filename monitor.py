import os, re, time, sys, signal
from datetime import datetime
delay = 1
failures = 0
tolerance = 1
host = "1.1.1.1"
separator = "---------------------------"
open('log.txt', 'a').close()

if len(sys.argv) - 1 != 1:
    print("No host given, defaulting to " + host)
else:
    host = str(sys.argv[1])

def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def write(message):
    with open("log.txt", "a") as log:
        log.write(message + "\n")
    print(message)
def ping():
    response = os.system("ping -c 1 -W 1 " + host + " 1> /dev/null 2> /dev/null")
    return response
def signal_handler(signal, frame):
    write("Stopped\t" + current_time())
    sys.exit(0)
def time_difference(start, end):
    d1 = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    return (d2 - d1).total_seconds()

signal.signal(signal.SIGINT, signal_handler)

write(separator)
write("Host: "+ host + "\nStarted\t" + current_time())
write(separator)

while True:
    if ping() != 0:
        failures += 1
        if failures == 1:
            first_failure = current_time()
    else:
        failures = 0
    time.sleep(delay)
    while failures > tolerance:
        write("Down\t" + first_failure)
        while ping() != 0:
            time.sleep(delay)
        write("Up\t" + current_time())
        downtime = time_difference(first_failure, current_time())
        write("Time\t" + str(round(downtime)) + " sec")
        write(separator)
        failures = 0
