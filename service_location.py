#!/usr/bin/env python3
#

__author__ = 'Karit @nzkarit'
__copyright__ = 'Copyright 2018 Karit'
__license__ = 'MIT'
__version__ = '0.1'

import argparse
import logging
import logging.config
import sqlite3
import urllib.request
import sys
import time
import json
import datetime


def argParser():
    description = 'This tool will collect all the Real Time Information (RTI) for a particular bus service in Wellington NZ, from the Metlink API'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-s', action='store', type=int, dest='serviceID', default=1, help='The serivce id for the bus service you would like to capture the data for. Default: %(default)s')
    parser.add_argument('-i', action='store', type=int, dest='interval', default=60, help='How often in seconds to requery the API. Default: %(default)s')
    parser.add_argument('-d', action='store', type=str, dest='db', default='service_location.db', help='The sqlite database to data in. Assumes it already has all the schema in place. Default: %(default)s')
    parser.add_argument('--url', action='store', type=str, dest='url', default='https://www.metlink.org.nz/api/v1/ServiceLocation/', help='The base URL for the data. Default: %(default)s')
    return parser.parse_args()

def connectToDB():
    """
    Connect to the sqlite database
    """
    try:
        filename = arguments.db
        logger.debug('Connecting to DB: %s' % (filename))
        global conn
        conn = sqlite3.connect(filename)
        logger.debug('Connected to DB')
    except Exception as error:
        logger.error('Error--> {}'.format(error))

def closeDB():
    """
    Closes conenction to the sqlite database
    """
    try:
        logger.debug('Closing DB')
        conn.close()
        logger.debug('Closed DB')
    except Exception as error:
        logger.error('Error--> {}'.format(error))

def monitor():
    url = arguments.url+str(arguments.serviceID)
    logger.debug('URL: %s' % (url))
    while True:
        try:
            timestamp = datetime.datetime.utcnow().isoformat()
            with urllib.request.urlopen(url) as response:
                data = response.read()
                encoding = response.info().get_content_charset('utf-8')
                jsonData = json.loads(data.decode(encoding))
                rows = []
                for service in jsonData['Services']:
                    row = {}
                    row['timestamp'] = timestamp
                    row['LastModified'] = jsonData['LastModified']
                    row['Code'] = service['Service']['Code']
                    row['TrimmedCode'] = service['Service']['TrimmedCode']
                    row['Name'] = service['Service']['Name']
                    row['Mode'] = service['Service']['Mode']
                    row['Link'] = service['Service']['Link']
                    row['RecordedAtTime'] = service['RecordedAtTime']
                    row['VehicleRef'] = service['VehicleRef']
                    row['ServiceID'] = service['ServiceID']
                    row['HasStarted'] = service['HasStarted']
                    row['DepartureTime'] = service['DepartureTime']
                    row['OriginStopID'] = service['OriginStopID']
                    row['OriginStopName'] = service['OriginStopName']
                    row['DestinationStopID'] = service['DestinationStopID']
                    row['DestinationStopName'] = service['DestinationStopName']
                    row['Direction'] = service['Direction']
                    row['Bearing'] = service['Bearing']
                    row['BehindSchedule'] = service['BehindSchedule']
                    row['VehicleFeature'] = service['VehicleFeature']
                    row['DelaySeconds'] = service['DelaySeconds']
                    row['Lat'] = service['Lat']
                    row['Long'] = service['Long']
                    rows.append(row)
                logToDB(rows)
        except Exception as error:
            logger.error('Error--> {}'.format(error))
        time.sleep(arguments.interval)

def logToDB(rows):
    try:
        c = conn.cursor()
        for row in rows:
            sql = 'INSERT INTO service_location_details (timestamp, LastModified, Code, TrimmedCode, Name, Mode, Link, RecordedAtTime, VehicleRef, ServiceID, HasStarted, DepartureTime, OriginStopID, OriginStopName, DestinationStopID, DestinationStopName, Direction, Bearing, BehindSchedule, VehicleFeature, DelaySeconds, Lat, Long) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            c.execute(sql, (row['timestamp'], row['LastModified'], row['Code'], row['TrimmedCode'], row['Name'], row['Mode'], row['Link'], row['RecordedAtTime'], row['VehicleRef'], row['ServiceID'], row['HasStarted'], row['DepartureTime'], row['OriginStopID'], row['OriginStopName'], row['DestinationStopID'], row['DestinationStopName'], row['Direction'], row['Bearing'], row['BehindSchedule'], row['VehicleFeature'], row['DelaySeconds'], row['Lat'], row['Long']))
        conn.commit()
        c.close()
    except Exception as error:
        logger.error('Error--> {}'.format(error))
        conn.rollback()
        c.close()

def main():
    global arguments
    arguments = argParser()
    
    global logger
    logging.config.fileConfig('logging_service_location.cfg')
    logger = logging.getLogger(__name__)
    logger.info('Starting service location')
    logger.info('Arguments: %s' % (arguments))

    connectToDB()
    
    try:
        monitor()
    except KeyboardInterrupt:
        closeDB()
        sys.exit(1)
    except Exception as error:
        logger.error('Error--> {}'.format(error))
        sys.exit(1)

if __name__ == "__main__":
    main()
