import pandas as pd
import string
from datetime import datetime
from datetime import timedelta
from enum import Enum
from FiboTrends import Fibo
import json

""" Get Data """
df = pd.read_csv('Data/GCG19_Daily_1990.csv', engine='python', skipfooter=1)
df['Date Time'] = pd.to_datetime(df['Date Time']) # Convert all dates to datetime objects

""" Set up variables """
numberOfCandlesToView = 220  # 220 -> month, 100 -> weekly, N/A -> daily  TODO: More testing needed for weekly and daily
swingIsLowestLow = True
running = True
rowOfLowestLow = ""
rowOfHighestHigh = ""
name = ""
trendLetterNames = list(string.ascii_uppercase)
suffix = trendLetterNames[0]
letterIndex = 0
numberIndex = 1
fiboSummary = []
trend = ""

startIndex = 0
endIndex = startIndex + numberOfCandlesToView
lastIndex = df['Date Time'].size - 1 # TODO: CONSIDER ADDING CHECK FOR TO SEE IF NEED TO SUBTRACT FOR FOOTER OR NOT 


""" Creating functions """
def addTerminalSpace(n):
        for x in range(n+1):
                print()

print("Started processing...")
addTerminalSpace(1)

""" Main Function """
while(running):
        
        if (( startIndex + numberOfCandlesToView) >= lastIndex):
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

                # Perform Fibo Calculations                  
                fiboPoint = Fibo(rowOfHighestHigh["High"], rowOfLowestLow["Low"])
                isTrendUp = fiboPoint.isTrendUp(rowOfHighestHigh, rowOfLowestLow)
                fiboPercents = fiboPoint.calculateFiboForTrend(isTrendUp)

                # Set name of trend      
                # 
                if (letterIndex > len(trendLetterNames) - 1):
                        letterIndex = 0              
                if (isTrendUp):
                        trend = "UP"
                        name = trendLetterNames[letterIndex] # TODO: What if all 26 characters are used?
                        letterIndex += 1

                else:
                        trend = "DOWN"
                        name = numberIndex
                        numberIndex += 1

                
                fiboPoint.setName(name)

                # Prepare Fibo info for JSON Storage              
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
                fiboSummary.append(fiboInfo) #TODO: Save data to json file

                addTerminalSpace(1)

                # Clear values for next Fibo Pair
                if(not swingIsLowestLow):
                        rowOfHighestHigh = "" #TODO: create enum and set this to something like EMPTY
                elif (swingIsLowestLow):
                        rowOfLowestLow = ""  
                
        if (endIndex == lastIndex):
                running = False
                print("Stopping processing since endDate equals lastDateInDataFrame")
                addTerminalSpace(1)


print (fiboSummary)

addTerminalSpace(1)
print("It works!")
addTerminalSpace(1)