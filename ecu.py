#ecu.py
from threading import Thread
import obd
import config

#Globals

rpm = 2738
speed = 0
coolantTemp = 0
engineLoad = 0
boost = 10
connection = None

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
        connection.watch(obd.commands.INTAKE_PRESSURE, callback=self.new_boost)

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
                
