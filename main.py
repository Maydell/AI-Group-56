import sys
import nltk
import anaphora

fact_grammar = """
    FACT1: {<NN.*><VB.*><JJ.*>}
    """

if len(sys.argv) < 2:
    print "Usage: python main.py <filename>"
    sys.exit(0)

# Read the filename
filename = sys.argv[1]
f = open(filename, "r")

text = f.read()

# Call anaphora resolution
text = anaphora.anaphora(text)
pos_tags = map(nltk.pos_tag, text)

print pos_tags

cp = nltk.RegexpParser(fact_grammar)
for sentence in pos_tags:
	result = cp.parse(sentence)
	print result
