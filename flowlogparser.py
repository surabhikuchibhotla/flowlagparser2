import csv
from collections import defaultdict
# first, have to import the protocol numbers and their corresponding keyword, going to import that as a dictionary
def parseprotocolnumbers(filepath):
    protocoldict = {} # create empty dict to store protocol numbers and corresponding keyword
    with open(filepath, "r", encoding="utf8") as file: # open protocol numbers file
        for line in file: # go through each line in the file
            parts = line.split() # split the line into parts based on whitespace -- always returns a list of strings 
            if len(parts) >=2 and parts[0].isdigit(): # make sure the line is the right one we want to look at - check that it has more than two parts and the first part is a number
                protocolnumber = parts[0].strip() # the protocol number is the first part
                protocolkeyword = parts[1].lower().strip() # the corresponding keyword is the second part
                protocoldict[protocolnumber] = protocolkeyword # add the protocol number and keyword into the dict
    return protocoldict # return the dict


def parselookuptable(lookup_file): # changing the lookuptable.csv to a dictionary for easier reference
    lookupdict = defaultdict(list) # create an empty dictionary
    with open(lookup_file, "r", encoding="utf8") as file2: # open the file
        reader = csv.DictReader(file2) # use csv.dictreader() to read the file as a dictionary -- ALWAYS returns values as strings
        for row in reader:
            key = (row['dstport'].strip(), row['protocol'].strip()) # so this goes through every row and stores the value of the columns dstport and protocol as the key in a tuple
            lookupdict[key].append(row['tag']) # this assigns the value of tag to the key, uses append in case there are more than one tags
            # if there was repeating keys, we would use lookup_dict[key].append(row["tag"]) to not overwrite the original tag value
    return lookupdict

# this function has to return the counts for each tag ( like how many times the tag was applied ) and also return counts for the different port and protocol combinations
def mainparser(sampleflowlogdata, protocoldict, lookupdict):
    tagcount = defaultdict(int) # creates a dict that automatically initializes missing keys with a default integer value of 0
    port_protocol_count = defaultdict(int) # creates a dict that automatatically initializes missing keys with a default integer value of 0
    untagged_count = 0

    with open(sampleflowlogdata, "r", encoding="ascii") as file: # opens the file
        for line in file: # goes through every line in the file
            parts = line.split() # splits the line based on whitespace characters
            if len(parts) < 14 or parts[0] != '2': # make sure line is valid, aka flow log data is valid
            # checks if it has less than 14 parts and the first part is not 2, then it is NOT valid
                continue # skips the rest of the current loop iteration and moves to next iteration

            dst_port = parts[5].strip() # gets the dstport number from each line using parts
            protocolnum = parts[7].strip() # gets the protocolnum from each line using parts
            protocolname = protocoldict.get(protocolnum, "unknown").lower().strip() # looks up protocol_num in the dict, and if its not found, it returns unknown

            key = (str(dst_port).strip(), str(protocolname).strip()) # creates a temporary key that is a tuple, of dstport and protocol name that is used for lookup
            # they are changed to a str val for consistency when looking up values to keep CONSISTENCYYY bc the lookupdict keys that are made in parselookuptable are strings
            tags = lookupdict.get(key, ["Untagged"]) # gets a list ( since the default dict is list ) of values AKA tags for each key ( which is a dstport and protocol combination)

            for tag in tags: # goes through every tag in tags, bc tags might contain more than one tag if the port and protocol num combinations have more than one tag
                tagcount[tag] += 1 # adds one for every tag thats seen, updates tags that are already existing
            
            if "Untagged" in tags: # check for untagged port/protocol entries
                untagged_count += 1 # increment total untagged count
                tagcount["Untagged"] += 1 # increments untagged occurences specifically 

            port_protocol_count[key] += 1 # adds port, protocol pair to the dictionary and incremements the value by 1

        return tagcount, port_protocol_count, untagged_count
        
def write_output(tagcount, port_protocol_count, untagged_count, output_file):
    with open(output_file, mode='w', encoding="ascii") as file:
        #tag count
        file.write("Tag Counts:\n")
        file.write("Tag, count\n")

        for tag, count in tagcount.items():
            file.write(f"{tag}, {count}\n")
        
        file.write("Port/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")

        for (port, protocol), count2 in port_protocol_count.items():
            file.write(f"{port}, {protocol}, {count2}\n")