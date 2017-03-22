from __future__ import print_function, absolute_import
from get_temp_humidity import setup, take_data
import argparse
from apscheduler.schedulers.blocking import BlockingScheduler
from influxdb import client as influxdb
from datetime import datetime


def setup_db(host='localhost', port='8086', user='root', password='root',
             db_name='env_sensor'):
    """
    Open the InfluxDB database, and create if it doesn't exist

    Parameters
    ----------
    host (string)
    port (int)
    user (string)
    password (string)
    db_name (string)

    Returns
    -------
    InfluxDBClient object
    """

    db = influxdb.InfluxDBClient(host, port, user, password)
    all_dbs_list = db.get_list_database()

    if db_name not in [str(x['name']) for x in all_dbs_list]:
        print("Creating db {0}".format(db_name))
        db.create_database(db_name)
    else:
        print("Using db {0}".format(db_name))
        db.switch_database(db_name)
    return db


def write_data(database, bus=None, test=False):
    """
    Take temp and humidity data from the sensor on `bus` and write it to the 
    InfluxDB database `database`

    Parameters
    ----------
    database: InfluxDBClient object to write into
    test: Use simulated data
    """

    h, tc, tf = take_data(bus, test)

    json_body = [
        {
            "measurement": "temp_humd",
            "time": datetime.utcnow(),
            "fields": {
                "tempC": tc,
                "tempF": tf,
                "humidity": h
            }
        }
    ]
    database.write_points(json_body)


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
    db = setup_db()

    if args.test:
        sched.add_job(lambda: write_data(db, test=True),
                      'interval', minutes=args.interval)
    else:
        bus = setup(args.port)
        sched.add_job(lambda: write_data(db, bus=bus),
                      'interval', minutes=args.interval)

    sched.start()
