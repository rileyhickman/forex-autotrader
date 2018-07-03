import requests
import numpy as np  
import time
import matplotlib
import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 
import matplotlib.dates as mdates
from matplotlib import style 
import matplotlib.animation as animation
import functools
import pandas as pd 
import sys

import csv

from bs4 import BeautifulSoup
import math

style.use('ggplot')

def percentChange(startPoint, currentPoint):
	try:
		x = ((float(currentPoint)-startPoint)/abs(startPoint))*100
		if x == 0.0:
			return 0.0000000001
		else:
			return x
	
	except:
		return 0.0000000001

#########################################################################

# read in the refernce pattern

# reference data
refpatternAr = []

# this is the pattern database
with open("EUR_USDpatterns.csv") as csvfile:
	reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
	for row in reader: # each row is a list
	    refpatternAr.append(row)

refperformAr = [] 
# refernce performance
with open("EUR_USDperformance.csv") as csvfile:
	reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
	for row in reader: # each row is a list
	    refperformAr.append(row)

#########################################################################

tickerAr = []

period = 2 
periodsOfInterest = 31


pricesAr = []

xaxisCount = 1

while True: 

	xaxisCount += 1
	xp = list(range(1,xaxisCount))	

	r = requests.get('http://webrates.truefx.com/rates/connect.html?f=html')
	# print the first 500 characters of the HTML

	#print(r.text[0:500])


	soup = BeautifulSoup(r.text, 'html.parser')

	#print(soup.prettify)



	results = soup.find_all('tr')
	resultsSpec = results[0]

	tickerAr = []

	for data in resultsSpec.find_all('td'):
		tickerAr.append(data.text)
		#print(data)

	
	bidFig = float(tickerAr[2])
	bidPoints = (float(tickerAr[3])/100000)
	bid = round(bidFig + bidPoints,5)

	askFig = float(tickerAr[4])
	askPoints = (float(tickerAr[5])/100000)
	ask = round(askFig + askPoints,5)

	price = round((bid+ask)/2,5)


	print('Symbol:', tickerAr[0])
	#print('Bid Figure: ', bidFig)
	#print('Bid Points: ', bidPoints) 
	#print('Bid:', bid)
	#print('Ask Figure: ', askFig)
	#print('Ask Points: ', askPoints) 
	#print('Ask:', ask)
	print('Price:', price)
	print('--------------------------------------------------')

	
	pricesAr.append(price)
	#print(pricesAr)

	if len(pricesAr) >= periodsOfInterest: 
		pricesAr.pop(0)
		xp = list(range(1,31))	

		perChangeAr = []
		for tick in pricesAr:
			pc = percentChange(pricesAr[0], tick)
			perChangeAr.append(pc)
		print(perChangeAr)
		print(len(perChangeAr))


		# compare the live percentage change array to the historical data in our reference database.

		last = perChangeAr[-1]
		predAr = []
		patFound = 0
		plotPatAr = []

		for refPattern in refpatternAr:
			#print(len(refPattern))
			simArray = []
			for i in range(1,30):
				simArray.append(abs(percentChange(perChangeAr[i-1], refPattern[i-1])))

			howSim = (np.sum(simArray))/30.00

			if howSim < 90:
				patFound = 1
				plotPatAr.append(refPattern) # append matching new pattern to array 

				refPatDex = refpatternAr.index(refPattern)
				performPredict = refperformAr[refPatDex] # this is the performance prediction from this matching pattern

				predAr.append(performPredict) # this is the prediction array

		print('There are',len(plotPatAr),'matching patterns')

		'''
		fig = plt.figure(figsize=(10,7))

		for patt in plotPatAr:
			plt.plot(xp, patt)

		#for pred in predAr:
			#plt.scatter(35, pred, c ='c', alpha=0.3)

		#plt.axhline(y=last, xmin=0, xmax=35, linewidth=1.0, color = 'r')

		#plt.scatter(40, actualOutcome, c='b', alpha=0.3, s=45)
		#plt.scatter(40, avgPredict, c=pcolor, alpha=0.3, s=45)
		plt.plot(xp, perChangeAr, '#54fff7', linewidth = 3)
		plt.grid(True)
		plt.show()
		'''

	time.sleep(period)
















