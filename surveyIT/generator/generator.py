from os import mkdir
from os.path import exists, dirname, join
from shutil import copy
import jinja2
from textx import metamodel_for_language, model as md
from ..language.meta_model import QuestionType
import datetime
import sys

def generate(model, output_path, overwrite):
    """
    Generates web-based surveys (HTML + CSS + JS) from surveyIT domain specific language

    Parameters: 
        model (Survey): textX model that represents the survey
        output_path (string): The output to generate to
        overwrite (boolean): Should overwrite output files 
    """

    now = datetime.datetime.now().strftime("%a, %b %d, %Y %X")

    this_folder = dirname(__file__)

    questions = md.get_children_of_type("Question", model.survey)
    question_types = [question.type for question in questions]
    question_types = set(question_types)
    
    # copy and rename templates for user-defined question types
    for qt in question_types:
        if(qt.template_path!=''):
            if not exists(qt.template_path):
                print('Error: Template path {} does not exist.'.format(qt.template_path))
                return
            else:
                copy(qt.template_path, join(this_folder, 'templates/'+qt.name+'.j2'))       

    # create output folders
    output_folder = join(output_path, 'generator_output')

    if not overwrite and exists(output_folder):
        print('-- Skipping: {}'.format(output_folder))
        return
    
    if not exists(output_folder):
        mkdir(output_folder)

    js_output_folder = join(output_path, 'generator_output/js')
    if not exists(js_output_folder):
        mkdir(js_output_folder)

    css_output_folder = join(output_path, 'generator_output/css')
    if not exists(css_output_folder):
        mkdir(css_output_folder)

    # initialize template engine
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(join(this_folder, 'templates')),
        trim_blocks=True,
        lstrip_blocks=True)

    template = jinja_env.get_template('survey_html.j2')

    f = open(join(output_folder, "%s.html" % model.survey.name), 'w')
    f.write(template.render(survey=model.survey, datetime=now))

    js_template = jinja_env.get_template('survey_js.j2')

    f = open(join(js_output_folder, 'index.js'), 'w')
    f.write(js_template.render(survey=model.survey, datetime=now))

    copy(join(this_folder, 'templates/styles.css'), css_output_folder)
   
if __name__ == "__main__":

    this_folder = dirname(__file__)
    
    if len(sys.argv) < 2:
        print('Error: Survey file is missing.')
    else:
        survey_file = sys.argv[1]

        survey_metamodel = metamodel_for_language('surveyIT')

        # build model
        model = survey_metamodel.model_from_file(survey_file)
        

        generate(model, this_folder, True)
        