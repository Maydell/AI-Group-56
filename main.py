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
# FACT6: Ada Lovelace is considered...

# Dicts of contradicting adjectives and verbs
contAdj = {"tall": ["short", "tiny"], "short": ["tall", "big"], "happy": ["sad", "angry"], "sad": ["happy"]}
contVerb = {"likes": ["dislikes", "hates"], "hates": ["likes", "loves"], "dislikes": ["likes", "loves"]}

# Grammatic rules
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

parsers = [nltk.RegexpParser(grammar1), nltk.RegexpParser(grammar2), nltk.RegexpParser(grammar3)]

# Dict to hold all found facts
results = {"FACT1": [], "FACT2": [], "FACT3": [], "FACT4": [], "FACT5": [], "FACT6": []}

# For all sentences
for sent in sents:
    # Tag with POS-tags
    tagged_sent = nltk.pos_tag(sent)
    for parser in parsers: # Run each parser
        parsed_sent = parser.parse(tagged_sent)
        results2 = analyze(parsed_sent)
        for result in results2["FACT1"]:
            results["FACT1"].append(result)
        for result in results2["FACT2"]:
            results["FACT2"].append(result)
        for result in results2["FACT3"]:
            results["FACT3"].append(result)
        for result in results2["FACT4"]:
            results["FACT4"].append(result)
        for result in results2["FACT5"]:
            results["FACT5"].append(result)
        for result in results2["FACT6"]:
            results["FACT6"].append(result)

# Find contradictions for FACT1
for result in results["FACT1"]:
    # Get list of contradicting adjectives
    conts = contAdj[result.what_property]
    for other in results["FACT1"]:
        for cont in conts:
            if other.what_property == cont: # We have a contradiction
                print(str(result.who) + " cannot be " + str(result.what_property) + " and " + other.what_property)

# Find contradictions for FACT3
for result in results["FACT3"]:
    # Get list of contradicting verbs
    conts = contVerb[result.what_relation]
    for other in results["FACT3"]:
        if other.what_entity == result.what_entity: # Relation to same entity
            for cont in conts:
                if other.what_relation == cont: # We have a contradiction
                    print(str(result.who) + " cannot " + str(result.what_relation) + " and " + str(other.what_relation) + " " + result.what_entity + " at the same time")

print("FACT1")
for result in results["FACT1"]:
    print(result)

print("FACT2")
for result in results["FACT2"]:
    print(result)

print("FACT3")
for result in results["FACT3"]:
    print(result)

print("FACT4")
for result in results["FACT4"]:
    print(result)

print("FACT5")
for result in results["FACT5"]:
    print(result)

print("FACT6")
for result in results["FACT6"]:
    print(result)
