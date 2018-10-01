#!/usr/bin/python

import csv
import os
import sys
from datetime import datetime


#Constant Declarations --> Change this to whatever column headers in the ACTUAL input file 
kLineTypeColumnHeaderName = "line_type"
kCarrierColumnHeaderName = "carrier"
kPrimaryReasonCodesColumnHeader = "reason_codes"
kVerifiedColumnHeaderName = "verified"
kTrue = "TRUE"
kFalse = "FALSE"

logFile = None
startTime = datetime.now()
formattedStartTime = startTime.strftime("%Y%m%d%H%M")
logFileOutputName = sys.argv[1].strip('Input/')

def logInfo( logMessage ):
    """Logs data to the log file."""
    global logFile

    if ( logFile == None ):
        logFile = open("quick_stats_checker_%s_%s.txt"%(logFileOutputName,formattedStartTime),"w")

    logFile.write(str(logMessage))
    logFile.write('\n')
    logFile.flush()

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

def analyzeRecords(allRows):
    #REPEATING Record or DUPLICATE is when first name and last name are the same, AND the phone number is same in the input
    verifiedTrueCount = 0
    verifiedFalseCount = 0 
    mobileLineTypeCount = 0
    landlineLineTypeCount = 0
    fixedVOIPs = 0
    nonFixedVOIPs = 0
    carriersDict = {}
    allInputRowsCount = len(allRows)

    verifiedMobileCount = 0 
    thisRowHasAtLeastOneMobile = 0 

    blankReasonCodesCount = 0
    primaryReasonCodesArray = []

    for row in allRows:
        ###VERIFIED CHECK
        if row[kVerifiedColumnHeaderName] == kTrue:
            verifiedTrueCount += 1
            if row[kLineTypeColumnHeaderName] == 'Mobile':
                verifiedMobileCount += 1
        elif row[kVerifiedColumnHeaderName] == kFalse:
            verifiedFalseCount += 1
        ###LINE TYPE CHECK 
        if row[kLineTypeColumnHeaderName] == 'Mobile':
            mobileLineTypeCount += 1
        elif row[kLineTypeColumnHeaderName] == 'Landline':
            landlineLineTypeCount += 1
        elif row[kLineTypeColumnHeaderName] == 'FixedVoIP':
            fixedVOIPs += 1
        elif row[kLineTypeColumnHeaderName] == 'NonFixedVoIP':
            nonFixedVOIPs += 1 
        ###Carrier CHECK 
        if row[kCarrierColumnHeaderName] not in carriersDict:
            carriersDict[row[kCarrierColumnHeaderName]] = 1
        elif row[kCarrierColumnHeaderName] in carriersDict:
            carriersDict[row[kCarrierColumnHeaderName]] += 1 

        ###Reason Codes Check
        if row[kPrimaryReasonCodesColumnHeader]:
            if row[kPrimaryReasonCodesColumnHeader] == '' or row[kPrimaryReasonCodesColumnHeader] == ' ':
                blankReasonCodesCount+=1
            for element in row[kPrimaryReasonCodesColumnHeader].split('|'):
                primaryReasonCodesArray.append(element)


    reportAnalytics("Reporting Analytics: ****************************")

    verifiedMsg = "%d rows are verified true. %d rows are verified false. %d rows are blank on verified."%(verifiedTrueCount, verifiedFalseCount, allInputRowsCount-verifiedTrueCount-verifiedFalseCount)
    reportAnalytics(verifiedMsg)

    lineTypeMessage = "%d rows are Mobile. %d rows are Landlines. %d rows are FixedVOIPs. %d rows are NonFixedVOIPs"%(mobileLineTypeCount, landlineLineTypeCount, fixedVOIPs, nonFixedVOIPs)
    reportAnalytics(lineTypeMessage)

    verifiedTruePercent = verifiedTrueCount/allInputRowsCount * 100
    verifiedFalsePercent = verifiedFalseCount/allInputRowsCount * 100
    nonVerifiedPercent = (allInputRowsCount-verifiedTrueCount-verifiedFalseCount)/allInputRowsCount * 100

    mobilePercent = mobileLineTypeCount/allInputRowsCount * 100
    landlinePercent = landlineLineTypeCount/allInputRowsCount * 100

    percentageFiguresMsg = "%d%% of total was verified True. %d%% of total was verified False. %d%% of total was not verified true/false (might be blank). \n%d%% of total was Mobile linetype. %d%% of total was Landline linetype."%(verifiedTruePercent, verifiedFalsePercent, nonVerifiedPercent, mobilePercent, landlinePercent)
    reportAnalytics(percentageFiguresMsg)

    reportAnalytics("\nThere are %d verified true mobile numbers on the primary input"%verifiedMobileCount)

    #Analyzing carriers
    for key in carriersDict:
        carrierMsg = "%d records came from carrier: %s"%(carriersDict[key],key)
        reportAnalytics(carrierMsg)

    reportReasonCodesAnalytics(primaryReasonCodesArray)


def reportAnalytics(msg):
    logInfo(msg)
    print(msg)

def reportReasonCodesAnalytics(reasonCodes):
    setOfUniqueReasonCodes = set(reasonCodes)
    for reasonCode in setOfUniqueReasonCodes:
        count = reasonCodes.count(reasonCode)
        reportAnalytics("Reason code %s appears %d times in the primary input"%(reasonCode, count))


def main( argv ):
    """Main entry point for processing the file."""
    if ( len(argv) > 1 ):
        csvInputFileName = argv[1]
        if ( os.path.exists(csvInputFileName) and os.path.isfile(csvInputFileName) ):
            reportAnalytics("******************************************************")
            reportAnalytics("Opening file...")
            (fileHandle,fileReader) = openCsvFile( csvInputFileName )
            fieldNames = getFieldNames( fileReader )
            # strippedSlashcsvInputFileName = csvInputFileName.replace('/', '')
            # csvOutFileName = "output_find_duplicate_records_%s_%s"%(formattedStartTime, strippedSlashcsvInputFileName)
            # (outHandle, fileWriter) = openCsvWriter( csvOutFileName, fieldNames )

            allRows = fileToList( fileReader )
            reportAnalytics("There are %d rows in the input csv file"%len(allRows))
            reportAnalytics("******************************************************")
            reportAnalytics("Processing ....")
            reportAnalytics("******************************************************")

            analyzeRecords(allRows)

            # fileWriter.writeheader()
            # for row in allRows:
            #     fileWriter.writerow( row )

            reportAnalytics("******************************************************")
            reportAnalytics("There are %d rows in the output csv file"%len(allRows))
            # outHandle.close()
            reportAnalytics("Processing complete.")
            endTime = datetime.now()
            reportAnalytics("Elapsed time: " + str(endTime - startTime))
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
