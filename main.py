import sys
import nltk
import anaphora
from analysis import analyze

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
sents = anaphora.anaphora(text)
tagged_sents = map(nltk.pos_tag, text)

# print(tagged_sents)

# tagged_sents = nltk.corpus.brown.tagged_sents()
# sents = nltk.corpus.reuters.sents('training/9866') 

cp = nltk.RegexpParser(fact_grammar)
for sent in sents:
    tagged_sent = nltk.pos_tag(sent)
    parsed_sent = cp.parse(tagged_sent)
    print("\n> " + " ".join(sent) + "\n")
    analyze(parsed_sent)