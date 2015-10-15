import sys
import nltk
import anaphora

# FACT1: Stephan is tall, gree, blue and yellow
# FACT2: Stephan is 10 feet tall. Stephan is 40 years old.
# FACT3: Stephan likes green, blue and yellow apples.
# FACT4: Stephan killed a cat. Stephan killed Greg. Stephan is a man.
# FACT5: Stephan is dying.

fact_grammar = """
    FACT3: {<NN.*><VB.*>(<JJ.*>(<CC|,><JJ.*>)*)?<NN.*>}
    FACT1: {<NN.*><VB.*><JJ.*>(<CC|,>?<JJ.*>)*}
    FACT2: {<NN.*><VB.*><CD><NN.*><JJ.*>}
    FACT4: {<NN.*><VB.*><DT>?<JJ.*>?<NN.*>}
    FACT5: {<NN.*><VB.*><VB.*>}
    """

if len(sys.argv) < 2:
    print("Usage: python main.py <filename>")
    sys.exit(0)

# Read the filename
filename = sys.argv[1]
f = open(filename, "r")

text = f.read()

# Call anaphora resolution
text = anaphora.anaphora(text)
pos_tags = map(nltk.pos_tag, text)

# print(pos_tags)

results = []

cp = nltk.RegexpParser(fact_grammar)
for sentence in pos_tags:
    result = cp.parse(sentence)
    results.append(result)
    # print(result)

nouns = []

class HasPropertyRecord(object):
    """A database record meaning someone has some property"""
    def __init__(self, who, what_property):
        super(HasPropertyRecord, self).__init__()
        self.who = who
        self.what_property = what_property

    def __str__(self):
        return "Fact<" + self.who + " : " + self.what_property + ">"

for result in results:
    label = result[0].label()
    noun = result[0][0]
    # print(noun[0])

    if label == "FACT1":
        who = result[0][0][0]
        verb = result[0][1][0]
        if verb == "is":
            print("Found a fact where someone is something!")
            for (word, postag) in result[0][3:]:
                if postag == "JJ": # Just in case
                    record = HasPropertyRecord(who, word)
                    print(record)
        else:
            print("Couldn't udnerstand!")
            print(what)

