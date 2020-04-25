from textx import metamodel_from_file, TextXSyntaxError, TextXSemanticError
from textx.export import metamodel_export, model_export
import textx.scoping as scoping
import textx.scoping.providers as scoping_providers
import os

class QuestionType(object):
    def __init__(self, parent, name, description, parameters):
        self.parent = parent
        self.name = name
        self.description = description
        self.parameters = parameters

    def __str__(self):
        return self.name

class Parameter(object):
    def __init__(self, parent, name, required, parameter_type):
        self.parent = parent
        self.name = name
        self.required = required
        self.parameter_type = parameter_type

    def __str__(self):
        return self.name

def get_built_in_question_types():
    multiline_parameter = Parameter(None, 'multiline', True, 'boolean')
    text_question = QuestionType(None, 'TextQuestion', 'description', [multiline_parameter])

    options_parameter = Parameter(None, 'options', True, 'string[]')
    multiple_parameter = Parameter(None, 'multiple', True, 'boolean')
    choice_question = QuestionType(None, 'ChoiceQuestion', 'description', [options_parameter, multiple_parameter])

    min_parameter = Parameter(None, 'min', True, 'number')
    max_parameter = Parameter(None, 'max', True, 'number')
    min_description_parameter = Parameter(None, 'min_description', True, 'string')
    max_description_parameter = Parameter(None, 'max_description', True, 'string')
    linear_scale_question = QuestionType(None, 'LinearScaleQuestion', 'description', [min_parameter, max_parameter, min_description_parameter, max_description_parameter])

    built_in_objects =  {
        'multiline': multiline_parameter,
        'TextQuestion': text_question,
        'multiple': multiple_parameter,
        'ChoiceQuestion': choice_question,
        'min': min_parameter,
        'max': max_parameter,
        'min_description': min_description_parameter,
        'max_description': max_description_parameter,
        'LinearScaleQuestion': linear_scale_question,
    }

    return built_in_objects

def get_metamodel():

    current_path = os.path.dirname(__file__)
    grammar_path = os.path.relpath('../grammar/grammar.tx', current_path)

    metamodel = metamodel_from_file(grammar_path, classes=[Parameter, QuestionType], builtins=get_built_in_question_types())

    metamodel.register_scope_providers({
        "*.*": scoping_providers.PlainName(),
        "ParameterValue.name": scoping_providers.RelativeName(
            "parent.type.parameters"),
    })

    return metamodel
