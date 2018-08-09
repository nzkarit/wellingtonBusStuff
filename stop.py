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
    description = 'This tool will collect all the Real Time Information (RTI) for a particular bus stop in Wellington NZ, from the Metlink API'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-s', action='store', type=int, dest='stopID', default=5500, help='The stop number for the stop you would like to capture the data for. Default: %(default)s')
    parser.add_argument('-i', action='store', type=int, dest='interval', default=60, help='How often in seconds to requery the API. Default: %(default)s')
    parser.add_argument('-d', action='store', type=str, dest='db', default='stop.db', help='The sqlite database to data in. Assumes it already has all the schema in place. Default: %(default)s')
    parser.add_argument('--url', action='store', type=str, dest='url', default='https://www.metlink.org.nz/api/v1/StopDepartures/', help='The base URL for the data. Default: %(default)s')
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
    url = arguments.url+str(arguments.stopID)
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
                    row['Sms'] = jsonData['Stop']['Sms']
                    row['Lat'] = jsonData['Stop']['Lat']
                    row['Long'] = jsonData['Stop']['Long']
                    row['ServiceID'] = service['ServiceID']
                    row['IsRealtime'] = service['IsRealtime']
                    row['VehicleRef'] = service['VehicleRef']
                    row['Direction'] = service['Direction']
                    row['OperatorRef'] = service['OperatorRef']
                    row['OriginStopID'] = service['OriginStopID']
                    row['DestinationStopID'] = service['DestinationStopID']
                    row['AimedArrival'] = service['AimedArrival']
                    row['AimedDeparture'] = service['AimedDeparture']
                    row['ExpectedDeparture'] = service['ExpectedDeparture']
                    row['DisplayDeparture'] = service['DisplayDeparture']
                    row['VehicleFeature'] = service['VehicleFeature']
                    row['DepartureStatus'] = service['DepartureStatus']
                    row['DisplayDepartureSeconds'] = service['DisplayDepartureSeconds']
                    rows.append(row)
                logToDB(rows)
        except Exception as error:
            logger.error('Error--> {}'.format(error))
        time.sleep(arguments.interval)

def logToDB(rows):
    try:
        c = conn.cursor()
        for row in rows:
            sql = 'INSERT INTO stop_details (timestamp, LastModified, Sms, Lat, Long, ServiceID, IsRealtime, VehicleRef, Direction, OperatorRef, OriginStopID, DestinationStopID, AimedArrival, AimedDeparture, ExpectedDeparture, DisplayDeparture, VehicleFeature, DepartureStatus, DisplayDepartureSeconds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            c.execute(sql, (row['timestamp'], row['LastModified'], row['Sms'], row['Lat'], row['Long'], row['ServiceID'], row['IsRealtime'], row['VehicleRef'], row['Direction'], row['OperatorRef'], row['OriginStopID'], row['DestinationStopID'], row['AimedArrival'], row['AimedDeparture'], row['ExpectedDeparture'], row['DisplayDeparture'], row['VehicleFeature'], row['DepartureStatus'], row['DisplayDepartureSeconds']))
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
    logging.config.fileConfig('logging_stop.cfg')
    logger = logging.getLogger(__name__)
    logger.info('Starting stop')
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
