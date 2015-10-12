import sys
import nltk

fact_grammar = "FACT: {<LS|DT><JJ.*>*<NN.*>}"

if len(sys.argv) < 2:
    print "Usage: python main.py <filename>"
    sys.exit(0)

# Read the filename
filename = sys.argv[1]
file object = open(filename, "r")
