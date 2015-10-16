import model
import text2int

def analyze(parsed_sent):

    # print(parsed_sent)
    results = {"FACT1": [], "FACT2": [], "FACT3": [], "FACT6": []}

    # Not all attributes will have labels; we want to be resilient
    try:
        label = parsed_sent[0].label()
    except AttributeError:
        return results #should be empty

    if label == "FACT1":
        who = parsed_sent[0][0][0]
        verb = parsed_sent[0][1][0]
        if verb == "is":
            for (word, postag) in parsed_sent[0][2:]:
                if postag == "JJ": # Just in case
                    record = model.Property(who, word)
                    results["FACT1"].append(record)

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
        results["FACT2"].append(record)

    if label == "FACT3":
        who = parsed_sent[0][0][0]
        verb = parsed_sent[0][1][0]
        what = parsed_sent[0][-2][0]
        adjs = [word for (word,postag) in parsed_sent[0][2:-2] if postag == "JJ"]
        record = model.QualifiedRelation(who, verb, what, adjs)
        results["FACT3"].append(record)

    if label == "FACT4":
        who = parsed_sent[0][0][0]
        verb = parsed_sent[0][1][0]
        dt = None
        adj = None

        if len(parsed_sent[0] == 5):
            dt = parsed_sent[0][2][0]
            adj = parsed_sent[0][3][0]
            whom = parsed_sent[0][4][0]
        elif len(parsed_sent[0] == 4):
            if parsed_sent[0][2][1] == "DT":
                dt = parsed_sent[0][2][0]
            elif parsed_sent[0][2][1].startswith("JJ"):
                adj = parsed_sent[0][2][0]
            whom = parsed_sent[0][3][0]
        else:
            whom = parsed_sent[0][3][0]


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
        results["FACT6"].append(record)

    return results
