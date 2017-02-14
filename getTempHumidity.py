from __future__ import print_function
import argparse
import smbus
import sys
from apsheduler.schedulers.blocking import BlockingScheduler

def setup(i2c_port=1):
    bus = smbus.SMBus(i2c_port)

    try:
        bus.write_quick(0x27)
    except IOError as e:
        print("The device is not present. Check that it is plugged in correctly.")

    # give us a moment to take the data
    time.sleep(0.1)


def take_data():
    try:
        vals = bus.read_i2c_block_data(0x27, 0x0, 4)
        # extract data
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

    except IOError as e:
        print("The device was probably unplugged? Check connections.")

def parse_args():
    parser = argparse.ArgumentParser(description="Get temperature and humidity")
    parser.add_argument('--port', type=int, required=False, default=1,
            help='i2c port of temp/humidity sensor')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    setup(args.port)

    # setup the job on a schedule of once every minute
    sched = BlockingScheduler()
    sched.add_job(take_data, 'interval', minutes=1)
    sched.start()
