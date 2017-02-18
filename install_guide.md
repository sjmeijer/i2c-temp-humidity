# Install guide

The following instructions are for installing

1. InfluxDB (time series database for storing the data)
2. Grafana (dashboard for displaying data)
3. CollectD (Daemon for collecting system metrics)

## InfluxDB

Download influxDB from the official release page: https://portal.influxdata.com/downloads

```bash
wget https://dl.influxdata.com/influxdb/releases/influxdb_1.2.0_armhf.deb
sudo dpkg -i influxdb_1.2.0_armhf.deb

# start influx
sudo systemctl start influxdb
```

### Create a database

```bash
pi@raspberrypi:~ $ influx
Connected to http://localhost:8086 version 1.2.0
InfluxDB shell version: 1.2.0
> CREATE DATABASE test
> SHOW DATABASES
name: databases
name
----
_internal
test

> 
```


## Grafana
Using this github repo https://github.com/fg2it/grafana-on-raspberry/releases

```bash
wget https://github.com/fg2it/grafana-on-raspberry/releases/download/v4.1.2/grafana_4.1.2-1487023783_armhf.deb
sudo dpkg -i grafana_4.1.2-1487023783_armhf.deb
```

### Setup

```bash
# add to startup
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable grafana-server

# start
sudo /bin/systemctl start grafana-server
```

Configure Grafana through the dashboard at `localhost:3000` (user/pw: admin/admin)

You can add an influx datasource using the following:
```
url: http://localhost:8086
access:proxy

database: db_name
user/pw: root/root (probably should change)
```

The test when you save should be successful. 


# CollectD

sudo apt install collectd

## Getting collectd working with influxdb

Let collectd output to a network. Edit the config file: search for network plugin and uncomment, also
uncomment network section. In the network section remove everything except for the server and port. Make 
sure to remove client section, or will interfere with influxdb client

```bash
sudo vi /etc/collectd/collectd.conf
```

Similary edit the config for influxdb. Search for collectd stuff and uncomment. Ensure that the database 
it is sending to exsits, you may need to create it using the steps above.

```bash
sudo vi /etc/influxdb/influxdb.conf
```

You also may need to point to the correct types.db file, if it doesn't exist download it from the link below,
and update the reference in the influxdb config path

```bash
wget https://github.com/collectd/collectd/raw/master/src/types.db
# and move to the path in the config path
sudo mv types.db /usr/share/collectd/types.db
```

May also need to uncomment the top part in the the collectd config, need to check this to confirm.

## Manually starting everything up

```bash
# influxdb daemon
sudo influxd 

# collectd daemon
sudo collectd

# run influx
influx
```
