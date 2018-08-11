# Wellington Bus Stuff

This is a collection of tools for logging the Wellington Bus Real Time (RTI) information. This is collecting data from the Metlink API.

# Collecting Information for a Bus Stop's departures
stop_departures.py is a script that will collect all info for a bus stop and log it to a DB

```
$ ./stop_departures.py --help
usage: stop_departures.py [-h] [-s STOPID] [-i INTERVAL] [-d DB] [--url URL]
                          [-r REPEATS] [--dbtype {sqlite,mariadb}]
                          [--dbconfig DBCONFIGFILE]

This tool will collect all the Real Time Information (RTI) for a particular
bus stop in Wellington NZ, from the Metlink API

optional arguments:
  -h, --help            show this help message and exit
  -s STOPID             The stop number for the stop you would like to capture
                        the data for. Default: 5500
  -i INTERVAL           How often in seconds to requery the API. Default: 60
  -d DB                 The sqlite database to data in. Assumes it already has
                        all the schema in place. Only applicable if dbtype is
                        sqlite. Default: stop_departures.db
  --url URL             The base URL for the data. Default:
                        https://www.metlink.org.nz/api/v1/StopDepartures/
  -r REPEATS            How many time to repeat before exiting. 0 means repeat
                        forever. Default: 0
  --dbtype {sqlite,mariadb}
                        The type of database to use. Default: sqlite.
                        Available options: sqlite, mariadb
  --dbconfig DBCONFIGFILE
                        The configuration files that holds the database
                        connection details. Default: db.cfg

```

## SQL for a Bus stop
This are some SQL statements to get stats out of the data
### Most recent record for each service
```sql
SELECT *
	FROM stop_details sd1
	WHERE timestamp = (SELECT MAX(timestamp) FROM stop_details sd2 WHERE sd1.aimeddeparture = sd2.aimeddeparture)
```
### How many on time
```sql
SELECT departurestatus, COUNT(*)
	FROM stop_details sd1
	WHERE timestamp = (SELECT MAX(timestamp) FROM stop_details sd2 WHERE sd1.aimeddeparture = sd2.aimeddeparture)
	GROUP BY departurestatus
```
departurestatus | COUNT(*)
----------------|---------
null | 17
delayed | 1
onTime | 5

### How late are they?
```sql
SELECT serviceid, aimeddeparture, expecteddeparture, (CAST(strftime('%s', expecteddeparture) as integer) - CAST(strftime('%s', aimeddeparture) as integer)) AS delay
	FROM stop_details sd1
	WHERE timestamp = (SELECT MAX(timestamp) FROM stop_details sd2 WHERE sd1.aimeddeparture = sd2.aimeddeparture)
		AND expecteddeparture IS NOT NULL
	ORDER BY serviceid, aimeddeparture
```

# Collecting Service Location Information
service_location.py is a script that will collect all info for a bus service and log it to a DB

```
$ ./service_location.py --help
usage: service_location.py [-h] [-s SERVICEID] [-i INTERVAL] [-d DB]
                           [--url URL] [-r REPEATS]
                           [--dbtype {sqlite,mariadb}]
                           [--dbconfig DBCONFIGFILE]

This tool will collect all the Real Time Information (RTI) for a particular
bus service in Wellington NZ, from the Metlink API

optional arguments:
  -h, --help            show this help message and exit
  -s SERVICEID          The service id for the bus service you would like to
                        capture the data for. Default: 1
  -i INTERVAL           How often in seconds to requery the API. Default: 60
  -d DB                 The sqlite database to data in. Assumes it already has
                        all the schema in place. Only applicable if dbtype is
                        sqlite. Default: service_location.db
  --url URL             The base URL for the data. Default:
                        https://www.metlink.org.nz/api/v1/ServiceLocation/
  -r REPEATS            How many time to repeat before exiting. 0 means repeat
                        forever. Default: 0
  --dbtype {sqlite,mariadb}
                        The type of database to use. Default: sqlite.
                        Available options: sqlite, mariadb
  --dbconfig DBCONFIGFILE
                        The configuration files that holds the database
                        connection details. Default: db.cfg

```

The SQL query I am interested with this how far away from a bus when it drops off the list. I am seeing buses dropping off before they get to the stop so I want to quantify this.

# sqlite
To use sqlite you will need to copy the blanks into a working location, before running the scripts.
1. `cp stop_departures_blank.db stop_departures.db`
1. `cp service_location_blank.db service_location_blank.db`

# MariaDB

## Initial Setup
1. `sudo apt install mariadb-server python3-mysql.connector`
1. `sudo mariadb`
1. `create database bus;`
1. `use bus;`
1. `source schemas/stop_departures.mariadb.sql;`
1. `source schemas/service_location.mariadb.sql;`
1. `CREATE USER 'bus_input'@'localhost';`
1. `GRANT INSERT ON bus.* TO 'bus_input'@'localhost';`
1. `SET PASSWORD FOR 'bus_input'@'localhost' = PASSWORD('changeme');`

# Future
If you want it to do something please ask away or better still do a pull request with some code or some SQL in the Readme. Create an issue here or hit me up on Twitter @nzkarit
