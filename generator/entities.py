class Survey(object):

    def __init__(self, name, title, description, author):
        self.name = name
        self.title = title
        self.description = description
        self.author = author
        self.sections = []

class Section(object):
    
    def __init__(self, title, description):
        self.title = title
        self.description= description
        self.questions = []

class Question(object):

    def __init__(self, required, name, qtype, title):
        self.required = required
        self.name = name
        self.qtype = qtype
        self.title = title
        self.parameters= {}

   