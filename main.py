import sys
import nltk
import anaphora
from analysis import analyze
import model

# FACT1: Stephan is tall, gree, blue and yellow
# FACT2: Stephan is 10 feet tall. Stephan is 40 years old.
# FACT3: Stephan likes green, blue and yellow apples.
# FACT4: Stephan killed a cat. Stephan killed Greg. Stephan is a man.
# FACT5: Stephan is dying.

grammar1 = """
    FACT3: {<NN.*><VB.*>(<JJ.*>(<CC|,><JJ.*>)*)?<NN.*><\.>}
    FACT1: {<NN.*><VB.*><JJ.*>(<CC|,>?<JJ.*>)*}
    FACT2: {<NN.*><VB.*><CD><NN.*><JJ.*>}
    FACT5: {<NN.*><VB.*><VB.*><.>}
    """

grammar2 = """
    NP: {<NN.*>+}
    2V: {<VB.><VB.>}
    FACT6: {<NP.*><2V><IN|TO><.*>*<\.|,>}
"""

grammar3 = """
    NP: {<DT>?<JJ.*>?<NN.*>+}
    FACT4: {<NP.*><VB.*><NP.*><\.>}
"""

if len(sys.argv) < 2:
    print("Usage: python main.py <filename>")
    sys.exit(0)

sents = []
if sys.argv[1] == "brown":
    sents = nltk.corpus.brown.sents()
elif sys.argv[1] == "reuters":
    sents = nltk.corpus.reuters.sents() 
else:
    # Read the filename
    filename = sys.argv[1]
    f = open(filename, "r")

    text = f.read()

    # Call anaphora resolution
    sents = anaphora.anaphora(text)
    tagged_sents = map(nltk.pos_tag, text)

    # print(tagged_sents)

print(len(sents))

i = 0
parsers = [nltk.RegexpParser(grammar1), nltk.RegexpParser(grammar2), nltk.RegexpParser(grammar3)]
for sent in sents:
    tagged_sent = nltk.pos_tag(sent)
    for parser in parsers:
        parsed_sent = parser.parse(tagged_sent)
        results = analyze(parsed_sent)
        if len(results) > 0:
            for result in results:
                i += 1
                print(i, end=": ")
                print(result)