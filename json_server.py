"""
Serves a writes a basic JSON file, that is continuously updated
"""

from __future__ import print_function, absolute_import
import argparse
from apscheduler.schedulers.blocking import BlockingScheduler
import devices
import configparser


def write_data(devs, filename="/var/www/html/read.json"):
    """
    Collect JSON data from devices, and write to file

    Parameters
    ----------
    devices: (list)
        List of device objects with read_and_process() and write_json()
        functions
    filename: (string)
        JSON file to write out data to
    """
    text = []
    # print(devs)

    for device in devs:
        # print("Trying device: ", device)
        try:
            device.read_and_process()
            text += device.write_json(False)

        except Exception as e:
            print(e)

    with open(filename, 'w') as fh:
        fh.write(str(text))
        fh.close()

    return


def parse_args():
    parser = argparse.ArgumentParser(
        description="Read data from I2C Devices and write to JSON file")
    parser.add_argument("-f", "--filename", required=False,
                        help="Configuration file (default: config.ini)",
                        default="config.ini")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    sched = BlockingScheduler()

    devs = []

    config = configparser.ConfigParser()
    config.read(args.filename)

    device_names = config.sections()
    if not devices:
        print("You must specify some devices to read out. Quitting...")
        raise SystemExit(0)
    else:
        for device in device_names:
            d = config[device]
            print("Device:", device)
            labels = ["Type", "Description", "Port"]
            for i in labels:
                try:
                    print(i, ": ", d[i])
                except:
                    pass
            # actually load up the class
            devs.append(getattr(devices, d["Type"])(int(d["Port"])))
            devs[-1].description = d["Description"]

    print("Starting scheduler...")
    sched.add_job(lambda: write_data(devs=devs),
                  'interval', seconds=args.interval)

    sched.start()
