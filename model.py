class Property(object):
    """A database record meaning someone  some property"""
    def __init__(self, who, what_property):
        super(Property, self).__init__()
        self.who = who
        self.what_property = what_property
    def __str__(self):
        return "Property<" + self.who + " : " + self.what_property + ">"

class QuantifiedProperty(Property):
    """A database record meaning someone  some property with a value"""
    def __init__(self, who, what_property, how_much, units):
        super().__init__(who, what_property)
        self.how_much = how_much
        self.units = units
    def __str__(self):
        return "QuantifiedProperty<" + self.who + " : " + self.what_property + " (" + str(self.how_much) + " " + self.units + ")>"

class QualifiedProperty(Property):
    """A database record meaning someone  some property with a value"""
    def __init__(self, who, what_property, how):
        super().__init__(who, what_property)
        self.how = how
    def __str__(self):
        return "QualifiedProperty<" + self.who + " : " + self.what_property + "(" + self.how + ")>"

class QualifiedRelation(object):
    """A database record meaning someone  a relation to someone else"""
    def __init__(self, who, what_relation, what_entity, qualifications):
        super(QualifiedRelation, self).__init__()
        self.who = who
        self.what_relation = what_relation
        self.qualifications = qualifications
        self.what_entity = what_entity

    def __str__(self):
        str = "QualifiedRelation<" + self.who + " : " + self.what_relation + " : " + self.what_entity
        if len(self.qualifications) > 0:
            str += "(" + ", ".join(self.qualifications) + ")"
        str += ">"
        return str

class RelationToNoun:
    """A database record meaning someone  a relation to something"""
    def __init__(self, who, verb, dt, what):
        super(RelationToNoun, self).__init__()
        self.who = who
        self.verb = verb
        self.dt = dt
        self.what = what

    def __str__(self):
        return "RelationToNoun<" + self.who + " : " + self.verb + " " + self.dt + " " + self.what + ">"

class QuantifiedRelation:
    """A database record meaning someone  a relation to multiple entities"""
    def __init__(self, who, what_relation, num, whom):
        super(QuantifiedRelation, self).__init__()
        self.who = who
        self.what_relation = what_relation
        self.num = num
        self.whom = whom

    def __str__(self):
        return "QuantifiedRelation<" + self.who + " : " + self.what_relation + " " + self.num + " " + self.whom + ">"