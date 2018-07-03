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

import csv

import random


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


newpatternAr = []

# this is the new pattern that we will be searching for in our database
#example2 = [0.005105844, 0.003063506, 0.004084675, 0.003063506, 0.001021169, 0.045952597, 0.002042338, 0.011232857, 0.001021169, 0.009190519, -0.004084675, -0.003063506, -0.076587662, -0.106201558, -0.107222727, -0.093947532, -0.066375974, -0.03471974, -0.038804416, -0.047994935, -0.063312467, -0.049016104, -0.009190519, -0.051058441, -0.027571558, -0.029613896, -0.027571558, -0.029613896, -0.02859272, -0.030635065]
with open("AUD_CADpatterns.csv") as csvfile:
	reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
	for row in reader: # each row is a list
	    newpatternAr.append(row)


newperformAr = [] 
# refernce performance
with open("AUD_CADperformance.csv") as csvfile:
	reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
	for row in reader: # each row is a list
	    newperformAr.append(row)



def percentChange(startPoint, currentPoint):
	try:
		x = ((float(currentPoint)-startPoint)/abs(startPoint))*100
		if x == 0.0:
			return 0.0000000001
		else:
			return x
	
	except:
		return 0.0000000001


def patternRecognition():


	xp = list(range(1,31))	

	samps = 0
	accuracyAr = []
	highAccsamps = 0
	highAccAr = []

	matchThreshold = 100 # minumum number of patterns to be considered high probability


	for newPattern in newpatternAr: 
		newPatDex = newpatternAr.index(newPattern)
		newPerformDex = newPatDex
		last = newPattern[-1]

		predAr = []
		patFound = 0
		plotPatAr = []

		for refPattern in refpatternAr:

			simArray = [] 
			for i in range(1, 30): 
				simArray.append(abs(percentChange(newPattern[i-1], refPattern[i-1])))

			howSim = (np.sum(simArray))/30.00
			
			#print(howSim)
			if howSim < 40:
				patFound = 1
				
				plotPatAr.append(refPattern) # append matching new pattern to array 

				refPatDex = refpatternAr.index(refPattern)
				performPredict = refperformAr[refPatDex] # this is the performance prediction from this matching pattern

				predAr.append(performPredict) # this is the prediction array



		print('There are',len(plotPatAr),'matching patterns')
		#print('Corresponding to ', len(predAr),'predicted performaces.')

		avgPredict = (np.sum(predAr))/len(predAr) # this is the average prediction 		
		listactualOutcome =  newperformAr[newPerformDex] # actual prediction from the new pattern
		actualOutcome = listactualOutcome[0]



		if patFound == 1:
			samps += 1

			if avgPredict < last: 
				print('PUT...')
				print('Prediction:', avgPredict)
				print('Actual Outcome:', actualOutcome) 
				
				if actualOutcome < last: 
					print('Win!')
					pcolor = 'g'
					accuracyAr.append(100)
					if len(plotPatAr) >= matchThreshold:
						highAccsamps += 1
						highAccAr.append(100)
					else: 
						pass
				else: 
					print('Loss!')
					pcolor = 'red'
					accuracyAr.append(0)
					if len(plotPatAr) >= matchThreshold:
						highAccsamps += 1
						highAccAr.append(0)
					else: 
						pass

			if avgPredict > last: 
				print('CALL...')
				print('Prediction:', avgPredict)
				print('Actual Outcome:', actualOutcome) 
				if actualOutcome > last: 
					print('Win!')
					pcolor = 'g'
					accuracyAr.append(100)
					if len(plotPatAr) >= matchThreshold:
						highAccsamps += 1
						highAccAr.append(100)
					else: 
						pass
				else: 
					print('Loss!')
					pcolor = 'red'
					accuracyAr.append(0)
					if len(plotPatAr) >= matchThreshold:
						highAccsamps += 1
						highAccAr.append(0)
					else: 
						pass

			percentAccur = (np.sum(accuracyAr))/len(accuracyAr)
			print('Overall percent accuracy is', percentAccur, '%  after', samps, 'samples')

			highAccpercent = (np.sum(highAccAr))/len(highAccAr)
			print('High matching percent accuracy is', highAccpercent, '%  after', highAccsamps, 'samples')
			
			'''
			fig = plt.figure(figsize=(10,7))

			for patt in plotPatAr:
				plt.plot(xp, patt)

			for pred in predAr:
				plt.scatter(35, pred, c ='c', alpha=0.3)

			plt.axhline(y=last, xmin=0, xmax=35, linewidth=1.0, color = 'r')

			plt.scatter(40, actualOutcome, c='b', alpha=0.3, s=45)
			plt.scatter(40, avgPredict, c=pcolor, alpha=0.3, s=45)
			plt.plot(xp, newPattern, '#54fff7', linewidth = 3)
			plt.grid(True)
			plt.show()
			'''
			#time.sleep(2)
		else: 
			pass

		print('-------------------------------------------------------------------')



patternRecognition()














