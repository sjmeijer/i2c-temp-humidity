from __future__ import absolute_import
import time
from datetime import datetime
from .device import Device


class TC74(Device):

    def __init__(self, i2c_port, descr="TC74 Sensor"):
        Device.__init__(self)

        self.port = i2c_port

        self.test = False
        self.autoprocess = True

        self.device_name = "TC74"
        self.base_address = 0x48
        self.num_reads = 1
        self.bus = None
        self.description = descr

        self.tempC = 0
        self.tempF = 0

        self.setup()

    def setup(self):
        """
        Setup the bus to talk to the sensor

        Parameters
        ----------
        i2c_port (int, default=1)
        """
        import smbus
        bus = smbus.SMBus(self.port)

        self.bus = bus
        self.warmup()

        try:
            bus.write_quick(self.base_address)
        except IOError as e:
            print("The device is not present. Check that it is correctly connected")

        # give us a moment
        time.sleep(0.1)

        return bus

    def write_json(self, string=True):
        """
        Format the JSON for outputing the resulting data
        """

        theTime = time.mktime(time.localtime())

        json_body = [
            {
                "device": self.device_name,
                "time": theTime,
                "description": self.description,
                "port": self.port,
                "type": "temperature",
                "value": self.tempC,
                "unit": "C"
            }

        ]
        #	{'device': 'TC74', 'time': 12336677, 'value': 17, 'units': 'C',   'title': 'temperature'}
        #  [{"tempC": tc},{"unit": "C"},{"measurement":"temperature"}],

        if string:
            return str(json_body)
        else:
            return json_body

    def process_raw_values(self, values):
        """
        Processes the raw data taken from I2C device. 
        Data comes in the native format (an array of some N 8-bit words, usually)

        Parameters
        ----------
        values (python list):
                an array of 8-bit words, the raw output from a device

        Returns
        -------
        tempC (float): absolute temperature in degrees Celsius
        tempF (float): absolute temperature in degrees Fahrenheit

        """

        data = values[0] & 0xFF

        self.tempC = data
        self.tempF = (self.tempC * 9.0 / 5) + 32

        return

    def read_and_process(self):
        self.process_raw_values(self.simple_read())

        return
