# -------------------------------------------------------------------------------
# Name:        SharePriceProcessor
# Author:      Deepak Trama
#
# Created:     15/10/2014
# Purpose:     Implementation of a class which given data of share prices at different points in time
# returns the highest price and the corresponding time
#              Tested with Python 2.7
#-------------------------------------------------------------------------------

# TODO:
# Have an option to trim whitespace
# If we have two prices at different times, the first one is returned.
# validate that header row is present in csv file

import csv

#  class to process data provided in list of lists format containing price of share of companies
#  Parameters:
#    csvYearFieldIndex = 0 # zero based index of year in the list
#    csvMonthFieldIndex = 1 # zero based index of month in the list
#    csvCompanyFieldIndex = 2 # zero based index of first company in the list


class SharePriceProcessor:
    def __init__(self, yearindex=0, monthindex=1, companyindex=2):
        self.csvYearFieldIndex = yearindex
        self.csvMonthFieldIndex = monthindex
        self.csvCompanyFieldIndex = companyindex  # 0 based index for field in csv file

    # getMaxSharePrices processes data provided in list of lists format containing price of share of companies
    # returns dictionary with highest share price, year and month for each company with company name as key
    #
    # Parameters:
    # sharePriceData: list of lists
    #   the first row acts as a header and contains the company name followed by field data
    #   example:
    #    [
    #    ['Year', 'Month', 'Company-A', 'Company-B', 'Company-C', 'Company-D', 'Company-E'],
    #    [1990,     'Jan',  751,        552,            829,            289,    649]
    #    [1990,     'Feb',  503,        106,            877,            932,    691]
    #    [1990,     'Mar',  107,        170,            314,            206,    441]
    #    ]
    #
    #   Result returned for above input would look like this:
    #   {
    #       'Company A': 751, 1990, Jan
    #       'Company B': 552, 1990, Jan
    #       ...
    #   }
    def getMaxSharePrices(self, sharePriceData):
        headerRow = None
        priceList = {}
        for row in sharePriceData:
            if headerRow is None:
                headerRow = row
                continue
            year = int(row[self.csvYearFieldIndex])
            month = row[self.csvMonthFieldIndex]
            for i in range(self.csvCompanyFieldIndex, len(row)):
                if i > (len(headerRow) - 1):  # skip any extra fields in row
                    continue
                companyName = headerRow[i]
                sharePrice = int(row[i])
                if companyName in priceList:
                    if sharePrice > int(priceList[companyName][0]):
                        priceList[companyName] = (sharePrice, year, month)
                else:
                    priceList[companyName] = (sharePrice, year, month)
        return priceList


#  This class extends SharePriceProcessor by reading directly from a csv file
#  Parameters:
#    csvFileName: a file name usable by python's file open function
#    csvDelimiter, csvQuoteChar: parameters usable by python's csv reader to process the csv data
class SharePriceProcessorCsvFile(SharePriceProcessor):
    def getMaxSharePrices(self, csvFileName, csvDelimiter=',', csvQuoteChar='\n'):
        if csvFileName is None or csvFileName == '':
            raise ValueError('Csv FileName not specified')
        with open(csvFileName, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=csvDelimiter, quotechar=csvQuoteChar)
            return SharePriceProcessor.getMaxSharePrices(self, spamreader)
