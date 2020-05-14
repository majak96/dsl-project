class Survey(object):

    def __init__(self, name, title, description, author, submit_url, success_message, error_message):
        self.name = name
        self.title = title
        self.description = description
        self.author = author
        self.sections = []
        self.submit_url = submit_url
        self.success_message = success_message
        self.error_message = error_message

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

   