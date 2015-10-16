import model
import text2int

def analyze(parsed_sent):

    # print(parsed_sent)
    results = []

    # Not all attributes will have labels; we want to be resilient
    try:
        label = parsed_sent[0].label()
    except AttributeError:
        return results #should be empty

    if label == "FACT1":
        who = parsed_sent[0][0][0]
        verb = parsed_sent[0][1][0]
        if verb == "is":
            for (word, postag) in parsed_sent[0][3:]:
                if postag == "JJ": # Just in case
                    record = model.Property(who, word)
                    results.append(record)
    
    if label == "FACT2":
        who = parsed_sent[0][0][0]
        verb = parsed_sent[0][1][0]
        cardinal = parsed_sent[0][2][0]
        unit = parsed_sent[0][3][0]
        adj = parsed_sent[0][4][0]

        # if verb == "is":
        try:
            f = float(cardinal)
        except ValueError:
            f = text2int.convert(cardinal)
        record = model.QuantifiedProperty(who, adj, f, unit)
        results.append(record)

    if label == "FACT3":
        who = parsed_sent[0][0][0]
        verb = parsed_sent[0][1][0]
        what = parsed_sent[0][-2][0]
        adjs = [word for (word,postag) in parsed_sent[0][2:-2] if postag == "JJ"]
        record = model.QualifiedRelation(who, verb, what, adjs)
        results.append(record)

    if label == "FACT4":
        who = " ".join([word for (word,postag) in parsed_sent[0][0].leaves()])
        verb = parsed_sent[0][1][0]
        if type(parsed_sent[0][2]) is tuple:
            what = parsed_sent[0][2][0]
        else:
            what = " ".join([word for (word,postag) in parsed_sent[0][2].leaves()])
        record = model.SpecifiedRelation(who, verb, what)
        results.append(record)

    if label == "FACT5":
        print(parsed_sent)
        who = parsed_sent[0][0][0]
        what = parsed_sent[0][-2][0]
        record = model.Property(who, what)
        results.append(record)

    if label == "FACT6":
        who = " ".join(w for (w, p) in parsed_sent[0][0])
        verbs_property = " ".join(w for (w, p) in parsed_sent[0][1])
        how = []
        rem = parsed_sent[0][2:-1]
        for r in rem:
            if type(r) is tuple:
                how.append(r[0])
            else:
                for l in r.leaves():
                    how.append(l[0])
        how = " ".join(how)
        record = model.QualifiedProperty(who, verbs_property, how)
        results.append(record)
        
    return results