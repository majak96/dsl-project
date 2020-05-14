from os.path import dirname, join
from textx import language as lang

from .language.meta_model import get_survey_mm, get_question_types_mm

@lang("survey-dsl", "*.srvy")
def survey_lang():
    """
    A domain-specific language for defininig web-based surveys
    """
    return get_survey_mm()

@lang("question-types-dsl", "*.qstn")
def question_types_lang():
    """
    A domain-specific language for defininig new question types for surveys
    """
    return get_question_types_mm()