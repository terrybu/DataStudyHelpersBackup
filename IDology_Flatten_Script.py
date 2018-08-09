#!/usr/bin/python

import csv
import os
from datetime import datetime

"""Resolve duplicate numbers in Horizon Output File"""

logFile = None
startTime = datetime.now()
formattedStartTime = startTime.strftime("%Y%m%d%H%M")


def logInfo( logMessage ):
    """Logs data to the log file."""
    global logFile

    if ( logFile == None ):
        logFile = open("Logs/IDology_%s.txt"%formattedStartTime,"w")

    logFile.write(str(logMessage))
    logFile.write('\n')
    logFile.flush()

def openCsvFile( csvFileName ):
    """Opens a CSV Reader and returns it and the file handle for later closing."""
    csvfile = open(csvFileName, 'rb')
    fileReader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    return (csvfile,fileReader)

def openCsvWriter( csvFileName, fieldNames ):
    """Opens a CSV Writer and returns it and the file handle for later closing."""
    csvfile = open(csvFileName, 'wb')
    fileWriter = csv.DictWriter(csvfile, delimiter=',', quotechar='"', fieldnames=fieldNames)
    return (csvfile,fileWriter)

def getFieldNames( fileReader ):
    """Given a CSV file dictionary reader, returns the header field names from the CSV file."""
    return fileReader.fieldnames            

def fileToList( fileReader ):
    """Given a CSV file, this method returns an array composed of all the rows in that file."""
    rows = []
    for rowDictionary in fileReader:
        rows.append(rowDictionary)
    return rows

def findRowsWithMultiplePhoneNumbers(allRows):
    count = 0 
    multipleNumRowsArray = []
    for row in allRows:
        if ',' in row['phone_numbers']:
            multipleNumRowsArray.append(row)
            count += 1
    logInfo("Found %d rows with multiple phone numbers"%count)
    print("Found %d rows with multiple phone numbers"%count)

    logInfo(multipleNumRowsArray)

    additionalRowsCount = 0 
    for row in multipleNumRowsArray:
        phoneNumbersString = row['phone_numbers']
        numsArray =  phoneNumbersString.replace(" ","").split(',')
        for phoneNumber in numsArray:
            newRow = {}
            newRow['phone_numbers'] = phoneNumber
            newRow['first_name'] = row['first_name']
            newRow['last_name'] = row['last_name']
            allRows.append(newRow)
            additionalRowsCount += 1
        allRows.remove(row)
        
    logInfo("additional rows are %d rows"%additionalRowsCount)
    print("additional rows are %d rows"%additionalRowsCount)

def main( argv ):
    """Main entry point for processing the file."""
    if ( len(argv) > 1 ):
        csvInputFileName = argv[1]
        if ( os.path.exists(csvInputFileName) and os.path.isfile(csvInputFileName) ):
            print "Opening file..."
            (fileHandle,fileReader) = openCsvFile( csvInputFileName )
            fieldNames = getFieldNames( fileReader )
            csvOutFileName = "OUTPUT_IDology_Flatten_%s_%s"%(formattedStartTime, csvInputFileName)
            (outHandle, fileWriter) = openCsvWriter( csvOutFileName, fieldNames )

            allRows = fileToList( fileReader )
            print("There are %d rows in the input csv file"%len(allRows))
            logInfo("There are %d rows in the input csv file"%len(allRows))
            findRowsWithMultiplePhoneNumbers(allRows)

            fileWriter.writeheader()
            for row in allRows:
                fileWriter.writerow( row )

            print("There are %d rows in the output csv file"%len(allRows))
            logInfo("There are %d rows in the output csv file"%len(allRows))
            outHandle.close()
            print "Processing complete."
            endTime = datetime.now()
            print "Elapsed time: " + str(endTime - startTime)
        else:
            print "File does not exist, or is a directory!"
            print "usage: " + argv[0] + " {horizonFormatOutputFileName}"
            exit()
    else:
        print "Insufficient parameters!"
        print "usage: " + argv[0] + " {horizonFormatOutputFileName}"
        exit()

if __name__ == '__main__':
    import sys
    sys.exit(main( sys.argv ))
