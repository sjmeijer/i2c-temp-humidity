from __future__ import absolute_import
import time
from datetime import datetime
from .device import Device


class HIH8120(Device):

    def __init__(self, i2c_port):
        Device.__init__(self)

        self.test = False
        self.autoprocess = True

        self.base_address = 0x27
        self.num_reads = 4

        self.tempC = 0
        self.tempF = 0
        self.humidity = 0

    def setup(self):

        import smbus
        bus = smbus.SMBus(i2c_port)

        return

    def process_raw_values(self, values):
        return 1
