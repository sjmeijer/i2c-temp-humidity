import time
from datetime import datetime
from device import Device

class TC74(Device):

	def __init__(self, i2c_port):
		Device.__init__(self)

		self.port = i2c_port

		self.test = False
		self.autoprocess = True

		self.device_name = "TC74"
		self.base_address = 0x48;
		self.num_reads = 1

		self.tempC = 0
		self.tempF = 0


	def setup(self):
		"""
		Setup the bus to talk to the sensor

		Parameters
		----------
		i2c_port (int, default=1)
		"""
		import smbus
		bus = smbus.SMBus(self.port)

		try:
			bus.write_quick(self.base_address)
		except IOError as e:
			print("The device is not present. Check that it is correctly connected")

		# give us a moment
		time.sleep(0.1)
		return bus


	def write_json(self, bus):
		"""
		Format the JSON for outputing the resulting data
		"""
		
		json_body = [
		{
			"measurement": "temperature",
			"device": self.device_name,
			"time": datetime.utcnow(),
			"values":{
				"tempC": self.tempC,
				"tempF": self.tempF
			}
		}
		]
		#  [{"tempC": tc},{"unit": "C"},{"measurement":"temperature"}],

		return json_body

	def process_raw_values(self, values):
		"""
		Processes the raw data taken from I2C device. 
		Data comes in the native format (an array of some N 8-bit words, usually)
	
		Parameters
		----------
		values (python list):
			an array of 8-bit words, the raw output from a device

		Returns
		-------
		tempC (float): absolute temperature in degrees Celsius
		tempF (float): absolute temperature in degrees Fahrenheit

		"""

		data = values[0]&0xFF

		self.tempC = data
		self.tempF = (self.tempC * 9/5) + 32

