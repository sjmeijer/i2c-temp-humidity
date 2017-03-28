"""
Reads out data from the sensor and prints it to the terminal

"""

from __future__ import print_function, absolute_import
from get_temp_humidity import setup, take_data

from devices.TC74_device import TC74

import argparse
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def print_data(bus=None, test=False):
    """
    Take temp and humidity data from the sensor on `bus` and write it to the
    console

    Parameters
    ----------
    test: Use simulated data
    """
    h, tc, tf = take_data(bus, test)
    print("Temperature(F): %0.2f, Humidity: %0.2f" % (tf, h))
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

    if args.test:
        sched.add_job(lambda: print_data(test=True),
                      'interval', seconds=args.interval)
    else:
        dev = TC74(args.i2cport)

        sched.add_job(lambda: print_data(bus=bus),
                      'interval', seconds=args.interval)

    sched.start()
