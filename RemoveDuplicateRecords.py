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
        logFile = open("Logs/RemoveDuplicates_%s.txt"%formattedStartTime,"w")

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

def findRepeatingRecords(allRows):
    #REPEATING Record or DUPLICATE is when first name and last name are the same, AND the phone number is same in the input
    repeatingRecordsArray = [] 
    recordsFrequencyDictionary = {}
    for row in allRows:
        frequencyOfRecordRepeat = allRows.count(row)
        if frequencyOfRecordRepeat > 1:
            if frequencyOfRecordRepeat not in recordsFrequencyDictionary:
                recordsFrequencyDictionary[frequencyOfRecordRepeat] = []
            recordsFrequencyDictionary[frequencyOfRecordRepeat].append(row["phone_numbers"])
            repeatingRecordsArray.append(row)
    logInfo(recordsFrequencyDictionary)
    
    duplicationMathCount = 0 
    for key in recordsFrequencyDictionary:
        array = recordsFrequencyDictionary[key]
        frequencyMsg = "There are %d records that appear %d times in the file with same information"%(len(array),key)
        duplicationMathCount += len(array)/int(key)
        print(frequencyMsg)
        logInfo(frequencyMsg)
        print("******************************************************")

    logInfo(repeatingRecordsArray)
    msg = "There are a total of %d records that need to be deduplicated from the input file. With successful deduplication, output result should then count %d records less than the original input"%(len(repeatingRecordsArray),len(repeatingRecordsArray)-duplicationMathCount)
    logInfo(msg)
    print(msg)


def main( argv ):
    """Main entry point for processing the file."""
    if ( len(argv) > 1 ):
        csvInputFileName = argv[1]
        if ( os.path.exists(csvInputFileName) and os.path.isfile(csvInputFileName) ):
            print "Opening file..."
            print("******************************************************")
            (fileHandle,fileReader) = openCsvFile( csvInputFileName )
            fieldNames = getFieldNames( fileReader )
            csvOutFileName = "OUTPUT_IDology_Flatten_%s_%s"%(formattedStartTime, csvInputFileName)
            (outHandle, fileWriter) = openCsvWriter( csvOutFileName, fieldNames )

            allRows = fileToList( fileReader )
            print("There are %d rows in the input csv file"%len(allRows))
            logInfo("There are %d rows in the input csv file"%len(allRows))
            print("******************************************************")
            print("Processing ....")
            print("******************************************************")
            findRepeatingRecords(allRows)

            fileWriter.writeheader()
            for row in allRows:
                fileWriter.writerow( row )

            print("******************************************************")
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
