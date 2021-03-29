#ecu.py
from threading import Thread
import obd
import config

#Globals

rpm = 4000
speed = 0
coolantTemp = 0
engineLoad = 0
boost = 300
connection = None

def getTachImg():
    tachnum = 0
    if rpm < 250:
        tachnum = 0
    elif rpm < 500:
        tachnum = 1
    elif rpm < 750:
        tachnum = 2
    elif rpm < 1000:
        tachnum = 3
    elif rpm < 1250:
        tachnum = 4
    elif rpm < 1500:
        tachnum = 5
    elif rpm < 1750:
        tachnum = 6
    elif rpm < 2000:
        tachnum = 7
    elif rpm < 2250:
        tachnum = 8
    elif rpm < 2500:
        tachnum = 9
    elif rpm < 2750:
        tachnum = 10
    elif rpm < 3000:
        tachnum = 11
    elif rpm < 3250:
        tachnum = 12
    elif rpm < 3500:
        tachnum = 13
    elif rpm < 3750:
        tachnum = 14
    elif rpm < 4000:
        tachnum = 15
    elif rpm < 4250:
        tachnum = 16
    elif rpm < 4500:
        tachnum = 17
    elif rpm < 4750:
        tachnum = 18
    elif rpm < 5000:
        tachnum = 19
    elif rpm < 5250:
        tachnum = 20
    elif rpm < 5500:
        tachnum = 21
    elif rpm < 5750:
        tachnum = 22
    elif rpm < 6000:
        tachnum = 23
    elif rpm < 6250:
        tachnum = 24
    elif rpm < 6500:
        tachnum = 25
    elif rpm < 6750:
        tachnum = 26
    else:
        tachnum = 27
    return tachnum

class ecuThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        global connection
        ports = obd.scan_serial()
        print(ports)

        # Connect to ECU
        connection = obd.Async()

        # Setup which values to monitor.
        connection.watch(obd.commands.RPM, callback=self.new_rpm)
        connection.watch(obd.commands.SPEED, callback=self.new_speed)
        connection.watch(obd.commands.ENGINE_LOAD, callback=self.new_engine_load)
        connection.watch(obd.commands.BAROMETRIC_PRESSURE, callback=self.new_boost)

        # Start monitoring values
        connection.start()

        # Let the GUI know that the ecu is ready.
        config.ecuRead = True

    def new_rpm(self, r):
        global rpm
        rpm = int(r.value.magnitude)

    def new_speed(self, r):
        global speed
        speed = r.value.to("mph")
        speed = int(round(speed.magnitude))

    def new_engine_load(self, r):
        global engineLoad
        engineLoad = int(round(r.value.magnitude))

    def new_boost(self, r):
        global boost
        boost = int(round(r.value.magnitude) * 0.145038)
                
