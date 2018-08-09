import csv,argparse,sys

KEY_FIELD = "transaction_id"
VERIFY_FIELD = "verified"
MERGE_FIELDS = [VERIFY_FIELD, "RequestID", "DateEntered", "UniqueID", "FirstName", "LastName", "Address", "City", "State", "Zip", "MobilePhone", "Email", "Flag", "output-requestId", "phoneNumber", "status", "description", "additionalInfo", "transaction_id", "line_type", "carrier", "country_code", "short_code", "tenure", "msisdn_changes", "msisdn_change_from", "msisdn_change_from_on", "msisdn_change_to", "msisdn_change_to_on", "last_ported_on", "trust_indicator", "reason_codes", "verified", "streetNumber", "street", "city", "region", "postal3", "postal5", "postal9", "distance", "addressScore", "firstName", "lastName", "nameScore", "identifierDob", "identifierLast4", "updPhoneNumber", "updLineType", "updCarrier", "updCountryCode", "updVerified", "updTrustScore"]

def merge(orig_fh,new_fh,delim=',',allow_new_dupes=False):
    orig_reader = csv.DictReader(orig_fh,delimiter=delim)
    new_reader = csv.DictReader(new_fh,delimiter=delim)
    #make sure all the right fields exists
    for field in MERGE_FIELDS:
        if field not in orig_reader.fieldnames:
            raise Exception("Field %s expected in original file and not present" % field)
        if field not in new_reader.fieldnames:
            raise Exception("Field %s expected in new file and not present" % field)

    csvFileName = "merged_per_greg_script.csv"
    csvfile = open(csvFileName, 'wb')
    writer = csv.DictWriter(csvfile, delimiter=',', quotechar='"', fieldnames=orig_reader.fieldnames)
    writer.writeheader()
    new_trues = {}
    new_cnt = 0
    #read all verify=true records into a dict
    for row in new_reader:
        new_key = row[KEY_FIELD]
        #make sure there are no dupes in the new file
        if not allow_new_dupes and new_trues.has_key(new_key):
            raise Exception("Duplicate key: %s" % new_key)
        if row[VERIFY_FIELD].upper() == "TRUE":
            new_trues[new_key] = row
            new_cnt+=1
    replace_cnt = 0
    #replace all records in orig file with new results if key matches
    for row in orig_reader:
        if new_trues.has_key(row[KEY_FIELD]):
            new_row = new_trues[row[KEY_FIELD]]
            replace_cnt+=1
            for field in MERGE_FIELDS:
                row[field] = new_row[field]
        writer.writerow(row)
    #make sure the number or records that should be merged are
    if replace_cnt!=new_cnt:
        raise Exception("Number of replacements(%s) NOT EQUAL to number of verify=true in new file(%s)", (replace_cnt,new_cnt))
    print "Number of replacements(%s) EQUAL to number of verify=true in new file(%s)" % (replace_cnt,new_cnt)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("orig_file", help="the original file you wish to replace verify=false with verify=true")
    parser.add_argument("new_file", help="the file you have new verify=true which you wish to merge")
    parser.add_argument("-d", "--delimiter", help="the delimiter for both files", default=",")
    parser.add_argument("-k", "--key", help="use a diffenent key_field to join", default=KEY_FIELD)
    args = parser.parse_args()
    orig_fh = open(args.orig_file,'r')
    new_fh = open(args.new_file,'r')
    merge(orig_fh,new_fh,delim=args.delimiter)
    orig_fh.close()
    new_fh.close()