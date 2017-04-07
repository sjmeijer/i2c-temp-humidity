"""
Base device class
"""
from datetime import datetime


class Device:
    """
    Base device class that is inherited by all the other classes
    """

    def __init__(self):
        print("Initializing...")

        self.test = False
        self.autoprocess = True

        self.base_address = None  # this must be set correctly by the subclass
        self.num_reads = None  # this must be set correctly by the subclass
        self.bus = None				# this must be set

    def simple_read(self):
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
            self.warmup()
            try:
                vals = self.bus.read_i2c_block_data(
                    self.base_address, 0x0, self.num_reads)

                return vals

            except IOError as e:
                print(e)
                print(
                    "The device appears to have been disconnected. Check the connections.")

    def read_and_process(self):
        self.process_raw_values(self.simple_read())

        return

    def warmup(self):
        """
        Get the device ready to do a read
        """

        try:
            self.bus.write_quick(self.base_address)
        except Exception as e:
            print(e)
            print("The device is not present. Check that it is correctly connected")
