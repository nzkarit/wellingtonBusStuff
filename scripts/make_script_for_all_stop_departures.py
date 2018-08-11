#!/usr/bin/env python3
#

with open('../data/stops.txt', 'r') as infile:
        stops = infile.readlines()
        outfile = open('run_all_stops_departures.sh', 'w')
        outfile.write('#!/usr/bin/env sh\n')
        for stop in stops:
            outfile.write('/home/username/wellingtonBusStuff/stop_departures.py -s %s -r 1 --dbtype mariadb & \n' % (stop.strip()))
            outfile.write('sleep 1 \n')
