#!/usr/bin/env python

import json
import subprocess
import time

from datetime import datetime

rides = {
        'Breakers Edge':112,
        'Cocoa Cruiser':101,
        'Comet':3,
        'Farenheit':31,
        'Great Bear':1,
        'Laff Trakk':104,
        'Lightning Racer':2,
        'Sidewinder':10,
        'Skyrush':97,
        'sooperdooperLooper':11,
        'Storm Runner':83,
        'Trailblazer':28,
        'Wild Mouse':15,
        'Wildcat':13
    }
rides = sorted(rides.items(), key=lambda x:x[0])

# Loop here
while True:
    # Get current time
    currtime = datetime.now()
    # Don't run if park is closed
    h = currtime.hour
    m = currtime.minute
    if h >= 22:
        print "Park is closed"
        time.sleep(((12 - (24-h-1))*60 + (60-m))*60)
        continue
    elif h < 10:
        print "Park is closed"
        time.sleep(((10-h-1)*60 + (60-m))*60)
        continue
    try:
    # Download wait times
        url = 'hpapp.hersheypa.com/v1/rides/wait'
        subprocess.call('wget -O /home/pi/Desktop/hershey/waittimes.json {}'.format(url), shell=True)

        # Import wait times
        with open('/home/pi/Desktop/hershey/waittimes.json') as f:
            if f.read() == '':
                time.sleep(900)
                continue
            f.seek(0)
            d = json.load(f)
    except:
        time.sleep(900)
        continue

    # Parse the waits from json file
    waits = {}
    for key in d.keys():
        if key == 'closed': continue
        for ride in d[key]:
            id = ride['id']
            if key == 'wait':
                wait = ride['wait']
            else:
                wait = None
            waits[id] = wait

    # Print output
    ride_times = [waits[id] if id in waits else 'Missing' for (r, id) in rides]
    with open('/home/pi/Desktop/hershey/compiled_waits.txt', 'a') as g:
        g.write( "\t".join([str(x) for x in ([currtime.month, currtime.day, currtime.hour, currtime.minute, currtime.weekday()] + ride_times)]) + "\n")

    # Upload the output
    subprocess.call('/home/pi/Desktop/dropbox_uploader.sh upload /home/pi/Desktop/hershey/compiled_waits.txt .', shell=True)
    # Wait 15 minutes before next check
    time.sleep(900)
