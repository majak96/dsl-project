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

#checks if names of parameters in a question type are unique
#also checks if the name of a question type is the same as the predefined question type
def question_type_object_processor(question_type):

    builtin_question_types =['TextQuestion', 'ChoiceQuestion', 'DropDownQuestion', 'LinearScaleQuestion']

    if(question_type.name in builtin_question_types):
        raise TextXSemanticError('A predefined question type {} already exists!'.format(question_type.name))

    parameter_names = [parameter.name for parameter in question_type.parameters]
    
    for parameter_name in parameter_names:
        if parameter_names.count(parameter_name) > 1:
            raise TextXSemanticError('Parameter with the name {} already exists in the question type {}! Names of parameters in a question type must be unique.'.format(parameter_name, question_type.name))

#checks if all question names are unique
def survey_content_object_processor(survey_content):

    question_names = []
    for section in survey_content.sections:
        question_names.extend([question.name for question in section.questions])
        
    for question_name in question_names:
        if question_names.count(question_name) > 1:
            raise TextXSemanticError('Question with the name {} already exists! Question names must be unique.'.format(question_name))


#checks if all required parameters of the chosen question type are defined
#also checks if a value for a parameter has been defined more than once
def question_object_processor(question):

    parameters_in_question = [param.parameter for param in question.parameters]

    for parameter in question.type.parameters:
        if parameter.required == True and parameter not in parameters_in_question:
            raise TextXSemanticError('A required parameter {} of question type {} is missing from the question {}!'.format(parameter, question.type.name, question.name))

    for parameter in parameters_in_question:
        if parameters_in_question.count(parameter) > 1:
            raise TextXSemanticError('Parameter {} of question type {} has been defined twice in question {}'.format(parameter.name, question.type.name, question.name))

#checks if the type of the parameter value matches the defined parameter type
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
        raise TextXSemanticError('The type of the parameter {} of question type {} must be {}.'.format(parameter_value.parameter.name, parameter_value.parent.type.name, parameter_type))

def get_metamodel():

    current_path = os.path.dirname(__file__)
    grammar_path = os.path.relpath('../grammar/grammar.tx', current_path)

    object_processors = {
        'SurveyContent': survey_content_object_processor,
        'QuestionType': question_type_object_processor,
        'Question': question_object_processor,
        'ParameterValue': parameter_value_object_processor,
    }

    metamodel = metamodel_from_file(grammar_path, classes=[Parameter, QuestionType], builtins=get_built_in_question_types())

    metamodel.register_scope_providers({
        "*.*": scoping_providers.PlainName(),
        "ParameterValue.parameter": scoping_providers.RelativeName(
            "parent.type.parameters"),
    })

    metamodel.register_obj_processors(object_processors)

    return metamodel
    