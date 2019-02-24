import FiboTrends
import unittest

class TestFibo(unittest.TestCase):
    """ Test the methods in the Fibo module """

    def test_getName(self):
        """ Test that we can get the name of Fibo Object"""
        fiboPoint = FiboTrends.Fibo("1920.8", "681")
        result = fiboPoint.getName()
        self.assertEqual(result, "A")

    def test_setName(self):
        """ Test that we can set the name of Fibo Object"""
        fiboPoint = FiboTrends.Fibo("1920.8", "681")
        fiboPoint.setName("B")
        result = fiboPoint.getName()
        self.assertEqual(result, "B")

    def test_getTheHigh(self):
        """ Test that we can successfully get the high of Fibo Object """
        fiboPoint = FiboTrends.Fibo("1920.8", "681")
        result = fiboPoint.getTheHigh()
        self.assertEqual(result, 1920.8)
    
    def test_getTheLow(self):
        """ Test that we can successfully get the low of Fibo Object"""
        fiboPoint = FiboTrends.Fibo("1920.8", "681")
        result = fiboPoint.getTheLow()
        self.assertEqual(result, 681)

    def test_setTheHigh(self):
        """ Test that we can successfully set the high for Fibo Object """
        fiboPoint = FiboTrends.Fibo("1920.8", "681")
        fiboPoint.setTheHigh(435.3)
        result = fiboPoint.getTheHigh()
        self.assertEqual(result, 435.3)

    def test_setTheLow(self):
        """ Test that we can successfully set the set the low for Fibo Object """
        fiboPoint = FiboTrends.Fibo("1920.8", "681")
        fiboPoint.setTheLow(123)
        result = fiboPoint.getTheLow()
        self.assertEqual(result, 123)
    

    # def test_isTrendUp(self): #TODO: NEED TO IMPORT PANDAS
    #     """ Test that we can successfully set the set the low for Fibo Object """
    #     fiboPoint = FiboTrends.Fibo("A", "1920.8", "681")
    #     result = fiboPoint.isTrendUp()
    #     self.assertEqual(result, True)

    # def test_calculateFiboForTrend(self): #TODO:
    #     """ Test that Fibo Calculations are correct """
    #     fiboPoint = FiboTrends.Fibo("A", "1920.8", "681")
    #     result = fiboPoint.calculateFiboForTrend(True)
    #     self.assertEqual(result, [1449.676, 1300.9, 1152.124, 346.254, -87.676] )



if __name__ == '__main__':
    unittest.main()
