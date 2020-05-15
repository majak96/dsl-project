from os.path import dirname, join
from textx import language as lang
from textx import generator as gen

from .language.meta_model import get_survey_mm, get_question_types_mm
from .generator.generator import generate

@lang('surveyIT', '*.srvy')
def survey_lang():
    """
    A domain-specific language for defininig web-based surveys
    """
    return get_survey_mm()

@lang('question-types-dsl', '*.qstn')
def question_types_lang():
    """
    A domain-specific language for defininig new question types for surveys
    """
    return get_question_types_mm()

@gen('surveyIT', 'html+css+js')
def survey_gen(metamodel, model, output_path, overwrite, debug):
    """
    Generating web-based surveys (HTML + CSS + JS) from surveyIT
    """
    input_file = model._tx_filename
    outuput_dir = output_path if output_path else dirname(input_file)

    generate(model, outuput_dir, overwrite)
