import sys
import nltk
import anaphora
import text2int

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
        return "HasProperty<" + self.who + " : " + self.what_property + ">"

class HasPropertyWithValueRecord(HasPropertyRecord):
    """A database record meaning someone has some property with a value"""
    def __init__(self, who, what_property, how_much, units):
        super().__init__(who, what_property)
        self.how_much = how_much
        self.units = units
    def __str__(self):
        return "HasPropertyWithValue<" + self.who + " : " + self.what_property + " : " + str(self.how_much) + "(" + self.units + ")>"

class HasRelationToQualifiedEntity(object):
    """A database record meaning someone has a relation to someone else"""
    def __init__(self, who, what_relation, what_entity, qualifications):
        super(HasRelationToQualifiedEntity, self).__init__()
        self.who = who
        self.what_relation = what_relation
        self.qualifications = qualifications
        self.what_entity = what_entity

    def __str__(self):
        str = "HasRelationToQualifiedEntity<" + self.who + " : " + self.what_relation + " : " + self.what_entity
        if len(self.qualifications) > 0:
            str += "(" + ", ".join(self.qualifications) + ")"
        str += ">"
        return str

class HasRelationToNoun:
    """A database record meaning someone has a relation to something"""
    def __init__(self, who, verb, dt, what):
        super(HasRelationToNoun, self).__init__()
        self.who = who
        self.verb = verb
        self.dt = dt
        self.what = what

    def __str__(self):
        return "HasRelationToNoun<" + self.who + " : " + self.verb + " " + self.dt + " " + self.what + ">"

class HasRelationToEntities:
    """A database record meaning someone has a relation to multiple entities"""
    def __init__(self, who, what_relation, num, whom):
        super(HasRelationToEntities, self).__init__()
        self.who = who
        self.what_relation = what_relation
        self.num = num
        self.whom = whom

    def __str__(self):
        return "HasRelationToEntities<" + self.who + " : " + self.what_relation + " " + self.num + " " + self.whom + ">"

for result in results:
    label = result[0].label()
    noun = result[0][0]
    # print(noun[0])

    if label == "FACT1":
        who = result[0][0][0]
        verb = result[0][1][0]
        if verb == "is":
            for (word, postag) in result[0][3:]:
                if postag == "JJ": # Just in case
                    record = HasPropertyRecord(who, word)
                    print(record)
        else:
            print("Couldn't udnerstand!")
            print(what)
    
    if label == "FACT2":
        who = result[0][0][0]
        verb = result[0][1][0]
        cardinal = result[0][2][0]
        unit = result[0][3][0]
        adj = result[0][4][0]
        if verb == "is":
            try:
                f = float(cardinal)
            except ValueError:
                f = text2int.convert(cardinal)
            record = HasPropertyWithValueRecord(who, adj, f, unit)
            print(record)
        else:
            print("Couldn't udnerstand!")
            print(what)

    if label == "FACT3":
        who = result[0][0][0]
        verb = result[0][1][0]
        what = result[0][-1][0]
        adjs = [word for (word,postag) in result[0][2:-1] if postag == "JJ"]
        record = HasRelationToQualifiedEntity(who, verb, what, adjs)
        print(record)