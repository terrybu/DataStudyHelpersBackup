#!/usr/bin/python

import csv
import os
import sys
from datetime import datetime

def openCsvFile( csvFileName ):
    """Opens a CSV Reader and returns it and the file handle for later closing."""
    csvfile = open(csvFileName, 'r')
    fileReader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    return (csvfile,fileReader)

def openCsvWriter( csvFileName, fieldNames ):
    """Opens a CSV Writer and returns it and the file handle for later closing."""
    csvfile = open(csvFileName, 'w')
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

def unformatEveryPhoneNumber(allRows, writer):
    for row in allRows:
        unformattedNum = row['phone']
        newNum = "1" + unformattedNum.replace('(','').replace(')','').replace('-','').replace(' ','')
        row['phone'] = newNum
        writer.writerow(row)

def main( argv ):
    """Main entry point for processing the file."""
    if ( len(argv) > 1 ):
        csvInputFileName = argv[1]
        if ( os.path.exists(csvInputFileName) and os.path.isfile(csvInputFileName) ):
            print("Opening file...")
            print("******************************************************")
            (fileHandle,fileReader) = openCsvFile( csvInputFileName )
            fieldNames = getFieldNames( fileReader )
            csvOutFileName = "unformat_results.csv"
            (outHandle, fileWriter) = openCsvWriter( csvOutFileName, fieldNames )

            allRows = fileToList( fileReader )
            unformatEveryPhoneNumber(allRows, fileWriter)


            print("Writing complete.")

        else:
            print("File does not exist, or is a directory!")
            print("usage: " + argv[0] + " {horizonFormatOutputFileName}")
            exit()
    else:
        print("Insufficient parameters!")
        print("usage: " + argv[0] + " {horizonFormatOutputFileName}")
        exit()

if __name__ == '__main__':
    import sys
    sys.exit(main( sys.argv ))
