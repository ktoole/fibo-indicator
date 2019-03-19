import pandas as pd
import string
from datetime import datetime
from datetime import timedelta
from enum import Enum
from FiboTrends import Fibo
import csv

""" Set up variables """
EMPTY = ""
swingIsLowestLow = True
running = True
rowOfLowestLow = EMPTY
rowOfHighestHigh = EMPTY
name = EMPTY
trendLetterNames = list(string.ascii_uppercase)
suffix = trendLetterNames[0]
letterIndex = 0
numberIndex = 1
fiboSummary = []
trend = EMPTY
tenYearsInWeeks = 521
halfTheWindow = 2
csvName = ""
isValidTrend = True
previousHH = None
previousLL = None

""" Get Data """
df = pd.read_csv('../Data/GCG19_Weekly.csv', engine='python', skipfooter=1)
df['Date Time'] = pd.to_datetime(df['Date Time']) # Convert all dates to datetime objects

twentyOneYearsInMonths = 260
fivePointFiveYearsInWeeks = 286
DAILY = EMPTY
numberOfCandlesToView = fivePointFiveYearsInWeeks  #100 -> weekly, N/A -> daily  TODO: More testing needed for weekly and daily


startIndex = 0
endIndex = startIndex + numberOfCandlesToView
lastIndex = df['Date Time'].size - 1

TIMEFRAME = 'WEEKLY'

if (TIMEFRAME == 'WEEKLY'):
        startIndex = lastIndex - tenYearsInWeeks
        endIndex = startIndex + numberOfCandlesToView


""" Creating functions """
def addTerminalSpace(n):
        for x in range(n+1):
                print()

print('Started processing...')
addTerminalSpace(1)

""" Main Function """
while(running):

        if (( startIndex + numberOfCandlesToView) >= lastIndex):

                numberOfCandlesToView = numberOfCandlesToView // halfTheWindow
                endIndex = startIndex + numberOfCandlesToView

                if (numberOfCandlesToView <= 1):
                        endIndex = lastIndex

        else:
                endIndex = startIndex + numberOfCandlesToView

        # Create time window to view data
        dfTimeWindow = df.iloc[startIndex:endIndex]

        # Find highest high or lowest low
        if(swingIsLowestLow):
                lowestLowIndex = dfTimeWindow['Low'].idxmin()
                rowOfLowestLow = dfTimeWindow.loc[lowestLowIndex]
                startIndex = lowestLowIndex
                swingIsLowestLow = False
        else:
                highestHighIndex = dfTimeWindow['High'].idxmax()
                rowOfHighestHigh = dfTimeWindow.loc[highestHighIndex]
                startIndex = highestHighIndex
                swingIsLowestLow = True

        if((len(rowOfLowestLow)>0) and (len(rowOfHighestHigh)>0)):

                if ((rowOfHighestHigh['High'] == previousHH) and (rowOfLowestLow['Low'] == previousLL)):
                        # It's a duplicate
                        isValidTrend = False
                elif(rowOfHighestHigh['Date Time'] == rowOfLowestLow['Date Time']):
                        # They equal, meaning no real change in window
                        isValidTrend = False

                # Perform Fibo Calculations
                fiboPoint = Fibo(rowOfHighestHigh['High'], rowOfLowestLow['Low'])
                isTrendUp = fiboPoint.isTrendUp(rowOfHighestHigh, rowOfLowestLow)
                fiboPercents = fiboPoint.calculateFiboForTrend(isTrendUp)

                # Set name of trend
                if (letterIndex > len(trendLetterNames) - 1):
                        letterIndex = 0
                if (isTrendUp):
                        trend = 'UP'
                        name = trendLetterNames[letterIndex]
                        letterIndex += 1
                else:
                        trend = 'DOWN'
                        name = numberIndex
                        numberIndex += 1

                print()
                print("Start Index: ", startIndex)
                print("End Index: ", endIndex)
                print("Current Window Size: ", numberOfCandlesToView)
                print("isTrendUp: ", isTrendUp)
                print("Date of Low: ", rowOfLowestLow['Date Time'])
                print("Low: ", rowOfLowestLow['Low'])
                print("Date of High: ", rowOfHighestHigh['Date Time'])
                print("High: ", rowOfHighestHigh['High'])
                print()


                fiboPoint.setName(name)

                # Prepare Fibo info for CSV Storage
                fiboInfo = {
                        "Name": name,
                        "Trend": trend,
                        "Date of Low":  rowOfLowestLow['Date Time'],
                        "Date of High": rowOfHighestHigh['Date Time'],
                        "Low": rowOfLowestLow['Low'],
                        "High": rowOfHighestHigh['High'],
                        "38%": fiboPercents[0],
                        "50%":fiboPercents[1],
                        "62%":fiboPercents[2],
                        "127%":fiboPercents[3],
                        "162%":fiboPercents[4]
                }


                fiboSummary.append(fiboInfo)

                previousHH = fiboInfo["High"]
                previousLL = fiboInfo["Low"]

                # Clear values for next Fibo Pair
                if(not swingIsLowestLow):
                        rowOfHighestHigh = EMPTY
                elif (swingIsLowestLow):
                        rowOfLowestLow = EMPTY


        if (endIndex == lastIndex):
                running = False



# Create name of file based on timeframe
if (TIMEFRAME == 'MONTHLY'):
        csvName = 'monthly_results.csv'
elif (TIMEFRAME == 'WEEKLY'):
        csvName = 'weekly_results.csv'
elif (TIMEFRAME == 'DAILY'):
        csvName = 'daily_results.csv'


# Write results to output file
with open('../Output/' + csvName, 'w') as csvFile:
        columns = ['Name', 'Trend', 'Date of Low', 'Date of High', 'Low', 'High', '38%', '50%', '62%', '127%', '162%']
        writer = csv.DictWriter(csvFile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(fiboSummary)
print('Fibo results have been written to ' + csvName)

csvFile.close()

