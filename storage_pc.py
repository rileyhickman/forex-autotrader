import matplotlib
import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 
import matplotlib.dates as mdates
from matplotlib import style 
import numpy as np 
import time
import functools
import pandas as pd 
import sys


def percentChange(startPoint, currentPoint):
	try:
		x = ((float(currentPoint)-startPoint)/abs(startPoint))*100
		if x == 0.0:
			return 0.0000000001
		else:
			return x
	
	except:
		return 0.0000000001




def patternStorage(file):

	# formating of the csv data file

	df = pd.read_csv(file, parse_dates=True, 
							   			index_col='DateTime', 
							   			names=['Tid', 'Dealable', 'Pair', 'DateTime', 'Buy', 'Sell'])
	#df.drop(['lTid'], 1, inplace=True)
	del df['Tid']
	del df['Dealable']
	del df['Pair']


	bid = df['Buy'].values
	ask = df['Sell'].values

	allData = ((bid + ask) / 2) 

	patternAr = []
	performanceAr = []

	patStarttime = time.time()
	x = len(allData) - 60 
	y = 31

	while y < x: 
		pattern = []
		for i in range(1, 31):
			pattern.append(percentChange(allData[y-30], allData[y+(i-30)]))
	

		outcomeRange = allData[y+20:y+30] 
		currentPoint = allData[y]

		try: 
			avgOutcome = functools.reduce(lambda x, y: x+y, outcomeRange) / len(outcomeRange)
		except Exception as e: 
			print(str(e))
			avgOutcome = 0

		futureOutcome = percentChange(currentPoint, avgOutcome)

		patternAr.append(pattern)
		performanceAr.append(futureOutcome)

		y += 100

	print(patternAr)
	print(performanceAr)

	patterndf = pd.DataFrame(patternAr)
	patterndf.to_csv('AUD_CADpatterns.csv', index=False, header=False)

	performancedf = pd.DataFrame(performanceAr)
	performancedf.to_csv('AUD_CADperformance.csv', index=False, header=False)




# csv data file from Gain
file = 'AUD_CAD_Week1.csv'



patternStorage(file)
