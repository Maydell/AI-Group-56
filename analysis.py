import model
import text2int

def analyze(parsed_sent):

    # Not all attributes will have labels; we want to be resilient
    try:
        label = parsed_sent[0].label()
    except AttributeError:
        return

    if label == "FACT1":
        who = parsed_sent[0][0][0]
        verb = parsed_sent[0][1][0]
        if verb == "is":
            for (word, postag) in parsed_sent[0][3:]:
                if postag == "JJ": # Just in case
                    record = model.HasProperty(who, word)
                    print(record)
        else:
            print("Couldn't understand!")
            print(what)
    
    if label == "FACT2":
        who = parsed_sent[0][0][0]
        verb = parsed_sent[0][1][0]
        cardinal = parsed_sent[0][2][0]
        unit = parsed_sent[0][3][0]
        adj = parsed_sent[0][4][0]
        if verb == "is":
            try:
                f = float(cardinal)
            except ValueError:
                f = text2int.convert(cardinal)
            record = model.HasQuantifiedProperty(who, adj, f, unit)
            print(record)
        else:
            print("Couldn't understand!")
            print(what)

    if label == "FACT3":
        who = parsed_sent[0][0][0]
        verb = parsed_sent[0][1][0]
        what = parsed_sent[0][-1][0]
        adjs = [word for (word,postag) in parsed_sent[0][2:-1] if postag == "JJ"]
        record = model.HasQualifiedRelation(who, verb, what, adjs)
        print(record)