# i2c-temp-humidity
A simple I2C temperature humidity sensor readout in python for use on a
Raspberry Pi.

## Files

1. `get_temp_humidity.py`: Read data from sensor
2. `influxdb_server.py`: Writes data from sensor to influxDB
    For details run influxdb_server.py --help or view source

## Installation

For details setting up influxDB and Grafana (dasboard) see [install_guide.md](install_guide.md)

### Dependencies

1. get_temp_humidity.py
    a. smbus
2. influxdb_server.py
    a. apscheduler
    b. influxdb
    c. datetime

# Sensor
The HIH8120-021-001 is a Digital Humidity/Temperature Sensor are digital
output-type relative humidity (RH) and temperature sensors combined in the same
package. 

The output of this sensor is I2C.

The sensor used was purchased form
[Newark](http://www.newark.com/honeywell/hih8120-021-001/humidity-digital-2-rh-sip-4/dp/04X4284)
for about $9.

