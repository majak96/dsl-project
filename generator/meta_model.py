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

    choices_parameter = Parameter(None, 'choices', True, 'string[]')
    multiple_parameter = Parameter(None, 'multiple', True, 'boolean')
    choice_question = QuestionType(None, 'ChoiceQuestion', 'description', [choices_parameter, multiple_parameter])

    options_parameter = Parameter(None, 'options', True, 'string[]')
    dropdown_question = QuestionType(None, 'DropDownQuestion', 'description', [options_parameter])

    min_parameter = Parameter(None, 'min', True, 'integer')
    max_parameter = Parameter(None, 'max', True, 'integer')
    min_description_parameter = Parameter(None, 'min_description', True, 'string')
    max_description_parameter = Parameter(None, 'max_description', True, 'string')
    linear_scale_question = QuestionType(None, 'LinearScaleQuestion', 'description', [min_parameter, max_parameter, min_description_parameter, max_description_parameter])

    built_in_objects =  {
        'TextQuestion': text_question,
        'ChoiceQuestion': choice_question,
        'DropDownQuestion': dropdown_question,
        'LinearScaleQuestion': linear_scale_question,
    }

    return built_in_objects

def question_object_processor(question):

    for parameter in question.type.parameters:
        if parameter.required == True and parameter not in [param.parameter for param in question.parameters]:
            raise TextXSemanticError('A required parameter {} is missing from a {}.'.format(parameter, question.type))

def parameter_value_object_processor(parameter_value):

    parameter_type = parameter_value.parameter.parameter_type

    parameter_val = parameter_value.value.value

    if ((parameter_type == "string[]" and (type(parameter_val).__name__ != "list" or type(parameter_val[0]).__name__ != "str")) or
        (parameter_type == "integer[]" and (type(parameter_val).__name__ != "list" or type(parameter_val[0]).__name__ != "int")) or 
        (parameter_type == "float[]" and (type(parameter_val).__name__ != "list" or type(parameter_val[0]).__name__ != "float")) or
        (parameter_type == "boolean[]" and (type(parameter_val).__name__ != "list" or type(parameter_val[0]).__name__ != "bool")) or
        (parameter_type == "string" and (type(parameter_val).__name__ != "str")) or 
        (parameter_type == "integer" and (type(parameter_val).__name__ != "int")) or
        (parameter_type == "float" and (type(parameter_val).__name__ != "float")) or
        (parameter_type == "boolean" and (type(parameter_val).__name__ != "bool"))):
        raise TextXSemanticError('Parameter {} should be a {}.'.format(parameter_value.parameter.name, parameter_type))

def get_metamodel():

    current_path = os.path.dirname(__file__)
    grammar_path = os.path.relpath('../grammar/grammar.tx', current_path)

    object_processors = {
        'Question': question_object_processor,
        'ParameterValue': parameter_value_object_processor
    }

    metamodel = metamodel_from_file(grammar_path, classes=[Parameter, QuestionType], builtins=get_built_in_question_types())

    metamodel.register_scope_providers({
        "*.*": scoping_providers.PlainName(),
        "ParameterValue.parameter": scoping_providers.RelativeName(
            "parent.type.parameters"),
    })

    metamodel.register_obj_processors(object_processors)

    return metamodel
    