import sys
import nltk
import anaphora

fact_grammar = """
    FACT: {<LS|DT><JJ.*>*<NN.*><VB.*>*}
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

print text

cp = nltk.RegexpParser(fact_grammar)
result = cp.parse(tokenized)
print result
result.draw()
