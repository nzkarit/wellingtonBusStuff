#!/usr/bin/env python3
#

import csv
import pandas
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from collections import OrderedDict
import argparse

description = 'Graph Stuff'
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-c', action='store', type=str, dest='csv', required=True, help='The path to the CSV to graph.')
parser.add_argument('-p', action='store', type=str, dest='png', required=True, help='The output PNG path.')
parser.add_argument('-t', action='store', type=str, dest='title', required=True, help='The title for the graph.')
parser.add_argument('-y', action='store', type=str, dest='yaxis', required=True, help='The y axis for the graph.')
parser.add_argument('-x', action='store', type=str, dest='xaxis', required=True, help='The x axis for the graph.')
parser.add_argument('--transpose', action='store', type=str, dest='transpose', default=False, help='Does the table need to be transposed? Default: %(default)s')

args = parser.parse_args()

coltitles = []
rowtitles = []
with open(args.csv, newline='') as csvfile:
    rows = csv.DictReader(csvfile, delimiter='	')
    for row in rows:
        for key in row.keys():
            rowtitles.append(row[key])
            row.pop(key)
            break
        coltitles = []
        for item in row:
            coltitles.append(item)
        



df = pandas.read_csv(args.csv, delimiter='	', header=0, index_col=0)
df.reindex(pandas.to_datetime(df.index))
if args.transpose:
    df = df.transpose()
df.plot()
plt.ylabel(args.yaxis)
plt.xlabel(args.xaxis)
plt.title(args.title)
locs, labels = plt.xticks()
if args.transpose:
    plt.xticks(range(len(coltitles)), coltitles, rotation=15)
else:
    #plt.xticks(range(len(rowtitles)), rowtitles, rotation=15)
    pass
plt.legend(loc='best')
plt.savefig(args.png)