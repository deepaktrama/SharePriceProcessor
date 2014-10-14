# -------------------------------------------------------------------------------
# Name:        module1
# Author:      Deepak Trama
#
# Created:     15/10/2014
# Purpose:     Unit tests for sharePriceProcessor
#-------------------------------------------------------------------------------

import unittest

from SharePriceProcessor import SharePriceProcessor, SharePriceProcessorCsvFile


class SharePriceProcessorTests(unittest.TestCase):
    def testFileNameNotProvided(self):
        csvProcessor = SharePriceProcessorCsvFile()
        with self.assertRaises(ValueError):
            csvProcessor.getMaxSharePrices('')

    def testFileNotFound(self):
        csvProcessor = SharePriceProcessorCsvFile()
        with self.assertRaises(IOError):
            csvProcessor.getMaxSharePrices('abcs.csv')

    def testWithNoData(self):
        testData = [
            ['Year', 'Month', 'Company-A', 'Company-B', 'Company-C', 'Company-D', 'Company-E']
        ]
        csvProcessor = SharePriceProcessor()
        self.assertEqual(csvProcessor.getMaxSharePrices(testData), {})

    def testWithSingleRowForSingleCompany(self):
        testData = [
            ['Year', 'Month', 'Company-A'],
            [1990, 'Jan', 751]
        ]
        csvProcessor = SharePriceProcessor()
        results = csvProcessor.getMaxSharePrices(testData)
        self.assertEqual(len(results), 1)
        self.assertItemsEqual(results['Company-A'], [751, 1990, 'Jan'])

    def testWithSingleRowForMultipleCompanies(self):
        testData = [
            ['Year', 'Month', 'Company-A', 'Company-B', 'Company-C', 'Company-D', 'Company-E'],
            [1990, 'Jan', 751, 552, 829, 289, 649]
        ]
        csvProcessor = SharePriceProcessor()
        results = csvProcessor.getMaxSharePrices(testData)
        self.assertEqual(len(results), 5)
        self.assertItemsEqual(results['Company-A'], [751, 1990, 'Jan'])
        self.assertItemsEqual(results['Company-B'], [552, 1990, 'Jan'])
        self.assertItemsEqual(results['Company-C'], [829, 1990, 'Jan'])
        self.assertItemsEqual(results['Company-D'], [289, 1990, 'Jan'])
        self.assertItemsEqual(results['Company-E'], [649, 1990, 'Jan'])

    # Test case written for Csv file emailed by IndieComm / Manjunath Hegde to me at deepak.trama@gmail.com
    def testWithCsvFile(self):
        csvProcessor = SharePriceProcessorCsvFile()
        results = csvProcessor.getMaxSharePrices('test_shares_data.csv')
        self.assertEqual(len(results), 5)  # there are 5 companies in the csv file
        # check against numbers calculated by Spreadsheet app
        self.assertItemsEqual(results['Company-A'], [1000, 2000, 'Mar'])
        self.assertItemsEqual(results['Company-B'], [986, 2007, 'Mar'])
        self.assertItemsEqual(results['Company-C'], [995, 1993, 'Jun'])
        self.assertItemsEqual(results['Company-D'], [999, 2002, 'Apr'])
        self.assertItemsEqual(results['Company-E'], [997, 2008, 'Oct'])
