class device():
	def __init__(self):
		print "initializing..."

		self.test = False
		self.autoprocess = True

		self.base_address = 0x0	# this must be set correctly by the subclass
		self.num_reads = 1	# this must be set correctly by the subclass



	def simple_read(self, bus, address, num_reads):
		"""
		Perform a single data read from the 0x0 register in the device

		Parameters
		----------
		bus (SMBus object): object should be conencted to the appropriate port
		address (int): the base address of the device, usually expressed in hex
		num_reads(int): the number of reads necessary to fully read out the device

		Returns
		-------
		vals (list): raw data words output by device
		"""
		
		if self.test:
			return take_test_data()
		else:
			try:
				vals = bus.read_i2c_block_data(address, 0x0, num_reads)
				
				return vals
		
			except IOError as e:
				print(e)
				print("The device appears to have been disconnected. Check the connections.")


	def

	def old_write_json(self):
		"""
		Format the JSON for outputing the data
		
		This function is not used, and will be removed shortly
		"""
	    	h, tc, tf = take_data(bus, test)

		json_body = [
        		{
            		"measurement": "temp_humd",
            		"time": datetime.utcnow(),
            		"fields": 
                		[{"tempC": tc},{"unit": "C"},{"measurement":"temperature"}],
                		"tempF": tf,
                		"humidity": h
            			
        		}
		]

	return json_body


