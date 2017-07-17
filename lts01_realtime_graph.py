#!/usr/bin/python

# Python library for LTS01A MLAB module with MAX31725 i2c Local Temperature Sensor

#uncomment for debbug purposes
#import logging
#logging.basicConfig(level=logging.DEBUG) 

import time
import datetime
import sys
from pymlab import config
import matplotlib.pylab as plt
import matplotlib.animation as animation
import numpy as np

#### Script Arguments ###############################################

'''
if len(sys.argv) != 2:
    sys.stderr.write("Invalid number of arguments.\n")
    sys.stderr.write("Usage: %s PORT ADDRESS\n" % (sys.argv[0], ))
    sys.exit(1)

port    = sys.argv[1]
'''
port = 1
address = 0x48
#### Sensor Configuration ###########################################

cfg = config.Config(
    i2c = {
        "port": port,
        "device": None,  # here you can explicitly set I2C driver with 'hid', 'smbus', 'serial'
    },

	bus = [
		{
            "type": "i2chub",
            "address": 0x72,

            "children": [
                {"name": "lts01", "type": "lts01", "address": address, "channel": 1, }
            ],
		},
	],
)

'''
cfg = config.Config(
    i2c = {
        "port": port,
    },
    bus = [
        {
            "name":          "lts01",
            "type":        "lts01",
            "address":        address,
        },
    ],
)
'''


cfg.initialize()

'''
print "LTS01A temperature sensor module example \r\n"
print "Temperature [deg C] \r\n"
'''
sensor = cfg.get_device("lts01")

#### Data Logging ###################################################

'''
try:
    while True:
        sys.stdout.write("LTS01A temp:" + str(sensor.get_temp()) + "\r\n")
        sys.stdout.flush()
        time.sleep(0.5)
except KeyboardInterrupt:
    sys.exit(0)
    '''

### PLOT PART

#setup figure
fig = plt.figure()
ax2 = fig.add_subplot(1,1,1)
#set up viewing window (in this case the 25 most recent values)
repeat_length = 100 
ax2.set_xlim([0,repeat_length])
ax2.set_ylim(top=30, bottom=20)

#set up list of images for animation
im2, = ax2.plot([], [], color=(0,0,1))

temp_collector = []
n_coll = []
def func(n):
    im2.set_xdata([n_coll])
    im2.set_ydata(temp_collector)
    temp_collector.append(sensor.get_temp())
    n_coll.append(n)
    if n>repeat_length:
        lim = ax2.set_xlim(n-repeat_length, n)
    else:
        # makes it look ok when the animation loops
        lim = ax2.set_xlim(0, repeat_length)
    return im2,

ani = animation.FuncAnimation(fig, func, frames=64000, interval=30, blit=False)

plt.show()
