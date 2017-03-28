class HIH8120(device):

	def __init__(self, i2c_port):
		device.__init__(self)

		self.test = False
		self.autoprocess = True

		self.base_address = 0x27
		self.num_reads = 4

		self.tempC = 0
		self.tempF = 0
		self.humidity = 0

	def setup(self):


		import smbus
		bus = smbus.SMBus(i2c_port)


	def process_raw_values(self, values):

