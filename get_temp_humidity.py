"""
Reads the temperature and humidity data from the sensor using the smbus library
"""
from __future__ import print_function, division
import time


def setup(i2c_port=1):
    """
    Setup the bus to talk to the sensor

    Parameters
    ----------
    i2c_port (int, default=1)
    """
    import smbus
    bus = smbus.SMBus(i2c_port)

    try:
        bus.write_quick(0x27)
    except IOError as e:
        print("The device is not present. Check that it is plugged in correctly.")

    # give us a moment before we start taking the data
    time.sleep(0.1)
    return bus


def take_data(bus, test=False):
    """
    Get single data readout from the sensor

    Parameters
    ----------
    bus (SMbus object):
        object should be connected to the appropriate port

    Returns
    -------
    humidity (float): % value
    tempC (float): absolute temperature in degrees Celsius
    tempF (float): absolute temperature in degrees Fahrenheit
    """
    if test:
        return take_test_data()
    else:
	    try:
	        vals = bus.read_i2c_block_data(0x27, 0x0, 4)
	        # data bytes as defined in datasheet
	        db1 = vals[0] & 0xFF
	        db2 = vals[1] & 0xFF
	        db3 = vals[2] & 0xFF
	        db4 = vals[3] & 0xFF

	        status = (db1 & 0xC0) >> 6
	        humidityRaw = db2 + ((db1 & 0x3F) << 8)
	        tempRaw = (db3 << 6) + ((db4 >> 2) & 0x3F)

	        humidity = (humidityRaw / 16383.0) * 100
	        tempC = (165 * (tempRaw / (16383.0))) - 40
	        tempF = (tempC * 9 / 5) + 32
	        return humidity, tempC, tempF

	    except IOError as e:
	        print("The device was probably unplugged? Check connections.")


def take_test_data():
    """
    Fake version of take_data() for testing, doesn't need to connect to 
    any physical device
    """
    import random
    tempC = random.uniform(10, 35)
    tempF = random.uniform(40, 100)
    humidity = random.uniform(40, 60)
    return humidity, tempC, tempF
