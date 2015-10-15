class HasProperty(object):
    """A database record meaning someone has some property"""
    def __init__(self, who, what_property):
        super(HasProperty, self).__init__()
        self.who = who
        self.what_property = what_property
    def __str__(self):
        return "HasProperty<" + self.who + " : " + self.what_property + ">"

class HasQuantifiedProperty(HasProperty):
    """A database record meaning someone has some property with a value"""
    def __init__(self, who, what_property, how_much, units):
        super().__init__(who, what_property)
        self.how_much = how_much
        self.units = units
    def __str__(self):
        return "HasQuantifiedProperty<" + self.who + " : " + self.what_property + " : " + str(self.how_much) + "(" + self.units + ")>"

class HasQualifiedRelation(object):
    """A database record meaning someone has a relation to someone else"""
    def __init__(self, who, what_relation, what_entity, qualifications):
        super(HasQualifiedRelation, self).__init__()
        self.who = who
        self.what_relation = what_relation
        self.qualifications = qualifications
        self.what_entity = what_entity

    def __str__(self):
        str = "HasQualifiedRelation<" + self.who + " : " + self.what_relation + " : " + self.what_entity
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

class HasQuantifiedRelation:
    """A database record meaning someone has a relation to multiple entities"""
    def __init__(self, who, what_relation, num, whom):
        super(HasQuantifiedRelation, self).__init__()
        self.who = who
        self.what_relation = what_relation
        self.num = num
        self.whom = whom

    def __str__(self):
        return "HasQuantifiedRelation<" + self.who + " : " + self.what_relation + " " + self.num + " " + self.whom + ">"