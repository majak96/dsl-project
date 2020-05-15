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

    # text question
    multiline_parameter = Parameter(None, 'multiline', True, 'boolean')
    min_char_parameter = Parameter(None, 'min_length', False, 'integer')
    max_char_parameter = Parameter(None, 'max_length', False, 'integer')
    placeholder_parameter = Parameter(None, 'placeholder', False, 'string')
    text_question = QuestionType(None, 'TextQuestion', 'description', [multiline_parameter, max_char_parameter, min_char_parameter, placeholder_parameter])

    # choice question
    choices_parameter = Parameter(None, 'choices', True, 'string[]')
    multiple_parameter = Parameter(None, 'multiple', True, 'boolean')
    choice_question = QuestionType(None, 'ChoiceQuestion', 'description', [choices_parameter, multiple_parameter])

    # drop down question
    options_parameter = Parameter(None, 'options', True, 'string[]')
    dropdown_question = QuestionType(None, 'DropDownQuestion', 'description', [options_parameter])

    # linear scale question
    min_value_parameter = Parameter(None, 'min_value', True, 'integer')
    max_value_parameter = Parameter(None, 'max_value', True, 'integer')
    min_description_parameter = Parameter(None, 'min_description', True, 'string')
    max_description_parameter = Parameter(None, 'max_description', True, 'string')
    linear_scale_question = QuestionType(None, 'LinearScaleQuestion', 'description', [min_value_parameter, max_value_parameter, min_description_parameter, max_description_parameter])

    # number question
    min_number_parameter = Parameter(None, 'min', False, 'integer')
    max_number_parameter = Parameter(None, 'max', False, 'integer')
    placeholder_number_parameter = Parameter(None, 'placeholder', False, 'string')
    number_question = QuestionType(None, 'NumberQuestion', 'description', [min_number_parameter,max_number_parameter, placeholder_number_parameter])
   
    # date question
    date_question = QuestionType(None, 'DateQuestion', 'description', [])

    # time question
    time_question = QuestionType(None, 'TimeQuestion', 'description', [])

    # likert scale question
    rows_names = Parameter(None, 'rows_names', True, 'string[]')
    columns_names = Parameter(None, 'columns_names', True, 'string[]')
    multiple_in_row = Parameter(None, 'multiple_in_row', True, 'boolean')
    likert_scale_question = QuestionType(None, 'LikertScaleQuestion', 'description', [rows_names, columns_names, multiple_in_row])

    built_in_objects =  {
        'TextQuestion': text_question,
        'ChoiceQuestion': choice_question,
        'DropDownQuestion': dropdown_question,
        'LinearScaleQuestion': linear_scale_question,
        'DateQuestion' : date_question,
        'TimeQuestion' : time_question,
        'LikertScaleQuestion' : likert_scale_question,
        'NumberQuestion' : number_question
    }

    return built_in_objects

def question_type_object_processor(question_type):
    """Checks if names of parameters in a question type are unique. 
    Also checks if the name of a question type is the same as the predefined question type."""

    builtin_question_types =['TextQuestion', 'ChoiceQuestion', 'DropDownQuestion', 'LinearScaleQuestion', 'DateQuestion', 'TimeQuestion', 'LikertScaleQuestion', 'NumberQuestion']

    if(question_type.name in builtin_question_types):
        raise TextXSemanticError('A predefined question type {} already exists!'.format(question_type.name))

    parameter_names = [parameter.name for parameter in question_type.parameters]
    
    for parameter_name in parameter_names:
        if parameter_names.count(parameter_name) > 1:
            raise TextXSemanticError('Parameter with the name {} already exists in the question type {}! Names of parameters in a question type must be unique.'.format(parameter_name, question_type.name))

def survey_content_object_processor(survey_content):
    """Checks if all question names are unique"""

    question_names = []
    for section in survey_content.sections:
        question_names.extend([question.name for question in section.questions])
        
    for question_name in question_names:
        if question_names.count(question_name) > 1:
            raise TextXSemanticError('Question with the name {} already exists! Question names must be unique.'.format(question_name))

def question_object_processor(question):
    """Checks if all required parameters of the chosen question type are defined.
    Also checks if a value for a parameter has been defined more than once."""

    parameters_in_question = [param.parameter for param in question.parameters]

    for parameter in question.type.parameters:
        if parameter.required == True and parameter not in parameters_in_question:
            raise TextXSemanticError('A required parameter {} of question type {} is missing from the question {}!'.format(parameter, question.type.name, question.name))

    for parameter in parameters_in_question:
        if parameters_in_question.count(parameter) > 1:
            raise TextXSemanticError('Parameter {} of question type {} has been defined twice in question {}'.format(parameter.name, question.type.name, question.name))


    # change parameters list to dictionary
    parameters_dict = {}
    for parameter in question.parameters :
        parameters_dict[parameter.parameter.name] = parameter.value.value

    question.parameters = parameters_dict

def parameter_value_object_processor(parameter_value):
    """Checks if the type of the parameter value matches the defined parameter type."""

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


def get_question_types_mm():
    """Returns the meta-model for question-types-dsl language."""

    current_dir = os.path.dirname(__file__)

    grammar_path = os.path.join(current_dir, 'question_types.tx')

    object_processors = {
        'QuestionType': question_type_object_processor
    }

    # build metamodel
    metamodel = metamodel_from_file(grammar_path, classes=[Parameter, QuestionType], builtins=get_built_in_question_types(), global_repository=True)

    metamodel.register_obj_processors(object_processors)

    return metamodel

def get_survey_mm():
    """Returns the meta-model for survey-dsl language."""

    current_dir = os.path.dirname(__file__)

    grammar_path = os.path.join(current_dir, 'survey.tx')

    object_processors = {
        'SurveyContent': survey_content_object_processor,
        'Question': question_object_processor,
        'ParameterValue': parameter_value_object_processor,
    }

    # build metamodel
    metamodel = metamodel_from_file(grammar_path, classes=[Parameter, QuestionType], builtins=get_built_in_question_types(), global_repository=True)

    metamodel.register_scope_providers({
        "*.*": scoping_providers.PlainNameImportURI(),
        "ParameterValue.parameter": scoping_providers.RelativeName(
            "parent.type.parameters"),
    })

    metamodel.register_obj_processors(object_processors)

    return metamodel