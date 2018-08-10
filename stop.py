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
    parser.add_argument('-r', action='store', type=int, dest='repeats', default=0, help='How many time to repeat before exiting. 0 means repeat forever. Default: %(default)s')
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
    i = 0
    while True:
        try:
            timestamp = datetime.datetime.utcnow().isoformat()
            logger.debug('Timestamp for: %s' % (timestamp))
            with urllib.request.urlopen(url) as response:
                data = response.read()
                encoding = response.info().get_content_charset('utf-8')
                jsonData = json.loads(data.decode(encoding))
                rows = []
                for service in jsonData['Services']:
                    row = {}
                    row['timestamp'] = timestamp
                    row['LastModified'] = jsonData['LastModified']
                    row['Name'] = jsonData['Stop']['Name']
                    row['Sms'] = jsonData['Stop']['Sms']
                    row['Farezone'] = jsonData['Stop']['Farezone']
                    row['Lat'] = jsonData['Stop']['Lat']
                    row['Long'] = jsonData['Stop']['Long']
                    row['ServiceID'] = service['ServiceID']
                    row['IsRealtime'] = service['IsRealtime']
                    row['VehicleRef'] = service['VehicleRef']
                    row['Direction'] = service['Direction']
                    row['OperatorRef'] = service['OperatorRef']
                    row['OriginStopID'] = service['OriginStopID']
                    row['OriginStopName'] = service['OriginStopName']
                    row['DestinationStopID'] = service['DestinationStopID']
                    row['DestinationStopName'] = service['DestinationStopName']
                    row['AimedArrival'] = service['AimedArrival']
                    row['AimedDeparture'] = service['AimedDeparture']
                    row['ExpectedDeparture'] = service['ExpectedDeparture']
                    row['DisplayDeparture'] = service['DisplayDeparture']
                    row['VehicleFeature'] = service['VehicleFeature']
                    row['DepartureStatus'] = service['DepartureStatus']
                    row['DisplayDepartureSeconds'] = service['DisplayDepartureSeconds']
                    row['Code'] = service['Service']['Code']
                    row['TrimmedCode'] = service['Service']['TrimmedCode']
                    row['ServiceName'] = service['Service']['Name']
                    row['Mode'] = service['Service']['Mode']
                    rows.append(row)
                logToDB(rows)
        except Exception as error:
            logger.error('Error--> {}'.format(error))
        if arguments.repeats > 0:
            i += 1
            logger.debug('%s of %s repeats' % (i, arguments.repeats))
            if i >= arguments.repeats:
                logger.info('Number of repeats reached, exiting')
                closeDB()
                sys.exit(0)
        logger.debug('Sleeping for: %s' % (arguments.interval))
        time.sleep(arguments.interval)

def logToDB(rows):
    logger.debug('Logging to DB')
    try:
        c = conn.cursor()
        for row in rows:
            sql = 'INSERT INTO stop_details (timestamp, LastModified, name, Sms, Farezone, Lat, Long, ServiceID, IsRealtime, VehicleRef, Direction, OperatorRef, OriginStopID, OriginStopName, DestinationStopID, DestinationStopName, AimedArrival, AimedDeparture, ExpectedDeparture, DisplayDeparture, VehicleFeature, DepartureStatus, DisplayDepartureSeconds, Code, TrimmedCode, ServiceName, Mode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            c.execute(sql, (row['timestamp'], row['LastModified'], row['Name'], row['Sms'], row['Farezone'], row['Lat'], row['Long'], row['ServiceID'], row['IsRealtime'], row['VehicleRef'], row['Direction'], row['OperatorRef'], row['OriginStopID'], row['OriginStopName'], row['DestinationStopID'], row['DestinationStopName'], row['AimedArrival'], row['AimedDeparture'], row['ExpectedDeparture'], row['DisplayDeparture'], row['VehicleFeature'], row['DepartureStatus'], row['DisplayDepartureSeconds'], row['Code'], row['TrimmedCode'], row['ServiceName'], row['Mode']))
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
