#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import logging
import urllib.request
import argparse

# Assert beautifulsoup is installed
try:
    from bs4 import BeautifulSoup
except ImportError:
    log.critical("It seems `beautifulsoup` is not installed. Please run pip install -r requirements.txt")
    sys.exit(1)

# Assert tabulate is installed
try:
    from tabulate import tabulate
except ImportError:
    log.critical("It seems `tabulate` is not installed. Please run pip install -r requirements.txt")
    sys.exit(1)

# Setup parameter
#   run script with -s, set sortby value
#   run script with -d, active debug mode (log file will be created)
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sort', choices=['Gold', 'Silver', 'Bronze', 'Total'], dest="sortby", help='sort results by number of Gold, Silver, Bronze or Total medals. Default: sort by Total')
parser.add_argument('-d', '--debug',  action='store_true', dest="debug", help='active debug log')
args = parser.parse_args()

# Config logging
logfile = 'Rio2016MedalTable.log' if args.debug == True else None
loglevel = logging.DEBUG if logfile is not None else None
logging.basicConfig(format='%(asctime)s [%(threadName)16s][%(module)14s][%(levelname)8s] %(message)s', filename=logfile, level=loglevel)

# Get sortby value if it exits
sortby = "Total" if args.sortby is None else args.sortby
logging.debug('sortby: ' + sortby)

# Define variable
#   url: official url for rio2016 medal table
#   dataSelectorDict: list of CSS selector pattern according to data for each column
#   printHeadList: list of header in printed table
url = 'https://www.rio2016.com/en/medal-count-country?rank=total'
dataSelectorDict = {
    'Country Code': 'td.col-2 > span.country',
    'Country Name': 'td.col-3 > span.country',
    'Gold':         'td.col-4',
    'Silver':       'td.col-5',
    'Bronze':       'td.col-6',
    'Total':        'td.col-7 > strong'
}
printHeadList = ['Rank', 'Country Code', 'Country Name', 'Gold', 'Silver', 'Bronze', 'Total']

# create http request
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
soup = BeautifulSoup(urllib.request.urlopen(req).read(), "html.parser")

# Construct row list from medal table
row = []
for data in soup.find_all('tr', class_='table-medal-countries__link-table'):
    tmpRes = {}
    for k,v in dataSelectorDict.items():
        logging.debug('Key: ' + k + ', Value: ' + v + ' :')
        logging.debug(data.select(v)[0])

        # Use CSS selector in beautifulsoup
        tmpRes[k] = (data.select(v)[0].renderContents().decode('utf-8').replace('\n', ''))

    row.append(tmpRes)

# Sort row list by sortby value first, then prio Gold > Silver > Bronze
sortedrow = sorted(row, key=lambda k: (int(k[sortby]), int(k['Gold']), int(k['Silver']), int(k['Bronze'])), reverse=True)
logging.debug(sortedrow)

# Construct printTableBody
#   printTableBody: list for printing, body part of table
#   currentRank: rank number, default 1
#   previewRank: preview cached rank number
#   currentMedalValue: weighted value based on gold, silver, bronze medals
#   previewMedalValue: preview cached medal value, default 0
printTableBody = []
currentRank = 1
previewRank = currentRank
previewMedalValue = 0
for r in sortedrow:
    tmpRow = []
    currentMedalValue = int(r['Gold']) * 1000000 + int(r['Silver']) * 1000 + int(r['Bronze']) * 1

    logging.debug('countryCode: ' + r['Country Code'])
    logging.debug('currentMedalValue: ' + str(currentMedalValue))
    logging.debug('previewMedalValue: ' + str(previewMedalValue))

    for l in printHeadList:
        # Set Rank value
        if l is 'Rank':
            # Medal value eq, then rank is eq
            if previewMedalValue == currentMedalValue:
                tmpRow.append(previewRank)
            # Medal value not eq, then use new rank
            else:
                tmpRow.append(currentRank)
                previewRank = currentRank
        else:
            tmpRow.append(r[l])
    previewMedalValue = currentMedalValue
    currentRank += 1
    printTableBody.append(tmpRow)

# Print results in a table
print(tabulate(printTableBody, printHeadList, tablefmt="grid"))
