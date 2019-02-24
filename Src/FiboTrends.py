class Fibo():

    def __init__(self, highestHigh, lowestLow):
        
        self.name = "A"
        self.highestHigh = float(highestHigh)
        self.lowestLow = float(lowestLow)

    def getName(self):
        return self.name
    
    def setName(self, theName):
        self.name = theName

    def getTheHigh(self):
        return self.highestHigh

    def setTheHigh(self, high):
        self.highestHigh = high
    
    def getTheLow(self):
        return self.lowestLow

    def setTheLow(self, low):
        self.lowestLow = low

    def isTrendUp(self, highCandle, lowCandle):
        """ Use dates of provided candles to deterine if it is an uptrend or downtrend """
        if (highCandle["Date Time"] > lowCandle["Date Time"]):

            return True
        elif (highCandle["Date Time"] < lowCandle["Date Time"]):
            return False

    def calculateOnlineNumber(self):
        """ Calculate the online numbers """
        onlineNumbers = []

        difference = self.highestHigh - self.lowestLow
        _38Percent = difference * 0.38
        _50Percent = difference * 0.50
        _62Percent = difference * 0.62
        _127Percent = difference * 1.27
        _162Percent = difference * 1.62

        onlineNumbers.extend([_38Percent, _50Percent, _62Percent, _127Percent, _162Percent])

        return onlineNumbers

    def calculateNextUpTrend(self, low, onlineNumbersList):
        """ Calculate the next uptrend """
        upTrendPercents = []

        _38Percent = onlineNumbersList[0] + low
        _50Percent = onlineNumbersList[1] + low
        _62Percent = onlineNumbersList[2] + low
        _127Percent = onlineNumbersList[3] + low
        _162Percent = onlineNumbersList[4] + low
        upTrendPercents.extend([_38Percent, _50Percent, _62Percent, _127Percent, _162Percent])
        
        return upTrendPercents

    def calculateNextDownTrend(self, high, onlineNumbersList):
        """ Calculate the next downtrend """

        downTrendPercents = []

        _38Percent = high - onlineNumbersList[0]
        _50Percent = high - onlineNumbersList[1]
        _62Percent = high - onlineNumbersList[2]
        _127Percent = high - onlineNumbersList[3]
        _162Percent = high - onlineNumbersList[4]

        downTrendPercents.extend([_38Percent, _50Percent, _62Percent, _127Percent, _162Percent])
        return downTrendPercents


    def calculateFiboForTrend(self, trendIsUp):
        """ Calculate the Fibo Percentages """

        low = self.lowestLow
        high = self.highestHigh
        
        onlineNumbers = self.calculateOnlineNumber()
    
        if(not trendIsUp):
            fiboPercents = self.calculateNextUpTrend(low, onlineNumbers)
        elif(trendIsUp):
            fiboPercents = self.calculateNextDownTrend(high, onlineNumbers)
        else:
            print("ERROR IN calculateFiboForTrend function")

        return fiboPercents




