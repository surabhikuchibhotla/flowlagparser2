import sys # for handling command-line arguments
import os # used to check if files exist
from flowlogparser import parseprotocolnumbers, parselookuptable, mainparser, write_output # imports all the functions from the file
def main():

    if len(sys.argv) != 5: # if the num of command line arguments are not FOUR, sys.arv includes main.py as one of the arguments
        print("Usage: python main.py <flow_log_file> <lookup_file> <protocol_file> <output_file>") # gives how youre supposed to use input 
        return
    
    flow_log_file = sys.argv[1] # assigns flowlogfile variable to the first file entered
    lookup_file = sys.argv[2] # assigns lookupfile variable to the second file entered
    iana_protocol_file = sys.argv[3] # assigns protocolfile variable to the third file entered
    output_file = sys.argv[4] # assigns outputfile variable to the fourth file entered

    if not all(os.path.exists(f) for f in [flow_log_file, lookup_file, iana_protocol_file]): # review how .os works
        print("Error: one or more input files are missing.")
        return
    protocoldict = parseprotocolnumbers(iana_protocol_file) # file not written in quotes bc its a variable not a string literal!
    lookupdict = parselookuptable(lookup_file) # does all the functions, corresponding with the names in flowlogparser.py ( confirm why that happens)
    tagcount, port_protocol_count, untagged_count = mainparser(flow_log_file, protocoldict, lookupdict)
    write_output(tagcount, port_protocol_count, untagged_count, output_file)

if __name__ == "__main__":
    main()