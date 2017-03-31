from __future__ import print_function, absolute_import
import argparse
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from devices.TC74_device import TC74
from devices.HIH8120 import HIH8120

def write_data(devs):
	
	text = []
	
#	print(devs)

	for device in devs:
#		print("Trying device: ", device)
		try:
			device.read_and_process()
			text += device.write_json(False)
	
		except Exception as e:
			print(e)



	with open('/var/www/html/read.json','w') as fh:
		fh.write(str(text))	
		fh.close()

	return


def parse_args():
	parser = argparse.ArgumentParser(
        description="Get temperature and humidity")
	parser.add_argument('--tc74', type=int, required=False, nargs='*')
	parser.add_argument('--hih8120', type=int, required=False, nargs='*')
	
#	parser.add_argument('--i2cport', type=int, required=False, default=1,
#                        help='i2c port of temp/humidity sensor')
	parser.add_argument('--interval', type=int, required=False, default=1,
                        help='interval (in seconds) to take data')

	parser.add_argument('--description', type=str, required=False, nargs='*',
						help='device description [--description tc74 0 "Cleanroom temperature"]')

	parser.add_argument("--f", dest="filename", required=False,
                    help="input file describing hardware", metavar="FILE")

	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	sched = BlockingScheduler()

	devs = []

	if(args.description):
		print(description)	

	if(args.tc74):
		for dd in args.tc74:
			print("Adding a TC74 device on port ",dd)
			devs.append(TC74(dd))
	if(args.hih8120):
		for dd in args.hih8120:
			devs.append(HIH8120(dd))

	if(args.filename):
		with open(args.filename,'r') as fh:
			fh.seek(0)
			for line in fh:
				if(len(line.split(',')) !=3):
					print("File incorrectly formatted at line: ",line)
						
				else:
					aDevice,aPort,aDescription = line.split(',')
					aPort = int(aPort)
					
					try:
						exec("d = %s(%d)" % (aDevice,aPort))
						devs.append(d)
						d.description = aDescription.rstrip()
						
					except Exception as e:
						print(e)

	if(len(devs) == 0):
		print("You must specify some devices to read out. Quitting...")
		raise SystemExit(0)




	sched.add_job(lambda: write_data(devs=devs),
                 'interval', seconds=args.interval)
	
	print("Starting scheduler...")
	sched.start()

