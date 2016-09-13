import smbus
import time
import datetime
import sys
import subprocess

def main():
	bus = smbus.SMBus(1)  # i2c port 1

	try:
		bus.write_quick(0x27)
	except IOError, e:
		#print e.errno
		#print e
		print "The device is not present. Check that it is plugged in correctly."
		makeWebPage(0,0,0)
		return [0,0]

	time.sleep(0.1)			# give us a moment to take the data
	try:
		vals =  bus.read_i2c_block_data(0x27,0x0,4)
	except IOError, e:
		print "The device was probably unplugged? Check connections."
		makeWebPage(0,0,0)
		return [0,0]

	ts = datetime.datetime.utcnow()

	# data bytes as defined in datasheet
	db1 = vals[0]&0xFF
	db2 = vals[1]&0xFF
	db3 = vals[2]&0xFF
	db4 = vals[3]&0xFF

	status = (db1&0xC0) >> 6
	humidityRaw = db2 + ((db1&0x3F)<<8)
	tempRaw = (db3<<6) + ((db4>>2)&0x3F)

	humidity = (humidityRaw/16383.0)*100
	tempC = (165*(tempRaw/(16383.0))) - 40
	tempF = (tempC*9/5)+32

	makeWebPage(ts,humidity, tempF)
#	print "temp: %03.3f, humidity: %03.3f" % (tempF, humidity)
	return [humidity,tempF]

def makeWebPage(ts,humidity,tempF):
	#fh = open('/home/pi/Documents/i2c_humidity/status.html','w')
	fh = open('/var/www/html/index.html','w')
	fh.write("<!DOCTYPE html>\n")
	fh.write('<html lang="en">\n')
	fh.write('	<head>\n')
	fh.write('		<meta charset="utf-8">\n')
	fh.write('		<title>Sensor Values</title>\n')
	fh.write('	</head\n>')
	fh.write('	<body>\n')
	fh.write("time: " + str(ts) + '<br>\n')
	fh.write("humidity: %.4f<br>\n" % (humidity))
	fh.write("temp: %.4f<br>\n" % (tempF))
	fh.write('	</body>\n')
	fh.write('</html>\n')

	fh.close()

if __name__ == "__main__":
	[h,tF] = main()
	st = "temp: " + str(tF) + " humidity: " + str(h)
	sys.stdout.write(st)
