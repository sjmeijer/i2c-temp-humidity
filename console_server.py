"""
Reads out data from the sensor and prints it to the terminal

"""

from __future__ import print_function, absolute_import
from get_temp_humidity import setup, take_data

from devices.TC74_device import TC74

import argparse
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def print_data(device):
	"""
	Take temp and humidity data from the sensor on `bus` and write it to the
	console

	Parameters
	----------
	device: the device class object that you wish to read out
	"""

	try:
		device.read_and_process()
	except Exception as e:
		print(e)

	print("Temperature(F): %0.2f" % (device.tempF))

	return


def parse_args():
    parser = argparse.ArgumentParser(
        description="Get temperature and humidity")
    parser.add_argument('--i2cport', type=int, required=False, default=1,
                        help='i2c port of temp/humidity sensor')
    parser.add_argument('--interval', type=int, required=False, default=1,
                        help='interval (in minutes) to take data')
    parser.add_argument('--test', type=bool, required=False, default=False,
                        help='test mode, not real hardware connection')
    return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	sched = BlockingScheduler()

	dev = TC74(args.i2cport)

	sched.add_job(lambda: print_data(device=dev),
				'interval', seconds=args.interval)

	sched.start()
