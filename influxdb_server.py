from __future__ import print_function, absolute_import
import argparse
from apscheduler.schedulers.blocking import BlockingScheduler
from influxdb import client as influxdb
from datetime import datetime
from devices.TC74_device import TC74


def setup_db(host='localhost', port=8086, user='root', password='root',
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
    all_dbs_list = db.get_database_list()

    if db_name not in [str(x['name']) for x in all_dbs_list]:
        print("Creating db {0}".format(db_name))
        db.create_database(db_name)
    else:
        print("Using db {0}".format(db_name))
        db.switch_database(db_name)
    return db


def write_data(database,device):
	"""
	Take temp and humidity data from the sensor on `bus` and write it to the 
	InfluxDB database `database`
	
	Parameters
	----------
	database: InfluxDBClient object to write into
	test: Use simulated data
	"""

	try:
		device.read_and_process()
		json_body = device.write_json(string=False)
	
	except Exception as e:
		print(e)

	database.write_points(json_body)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Get temperature and humidity")
    parser.add_argument('--i2cport', type=int, required=False, default=1,
                        help='i2c port of temp/humidity sensor (default 1)')
    parser.add_argument('--interval', type=int, required=False, default=30,
                        help='interval (in seconds) to take data (default 30)')
    return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	sched = BlockingScheduler()
   
	db = setup_db()
	dev = TC74(args.i2cport)

	sched.add_job(lambda: write_data(db, device=dev),
                 'interval', seconds=args.interval)

	sched.start()
