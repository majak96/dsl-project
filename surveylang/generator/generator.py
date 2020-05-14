from os import mkdir
from os.path import exists, dirname, join
from shutil import copy
import jinja2
from entities import Survey, Section, Question
from meta_model import get_metamodel
import datetime
import sys

def generate(survey_file):

    now = datetime.datetime.utcnow().strftime("%a, %b %d, %Y %X")
    
    this_folder = dirname(__file__)

    metamodel = get_metamodel()

    # build model
    model = metamodel.model_from_file(survey_file)

    survey_name = model.survey.name
    survey_information = model.survey.survey_info
    survey_object = Survey(survey_name,
                           survey_information.title,
                           survey_information.description,
                           survey_information.author,
                           survey_information.submit_url,
                           survey_information.success_message,
                           survey_information.error_message)

    for section in model.survey.sections :
        section_temp = Section(section.title, section.description)
        for question in section.questions :
            question_temp = Question(question.required,
                                     question.name,
                                     question.type.name, 
                                     question.title)
            for parameter in question.parameters :
                question_temp.parameters[parameter.parameter.name] = parameter.value.value
            section_temp.questions.append(question_temp)
        
        survey_object.sections.append(section_temp)

    # create output folders
    output_folder = join(this_folder, 'generator_output')
    if not exists(output_folder):
        mkdir(output_folder)

    js_output_folder = join(this_folder, 'generator_output/js')
    if not exists(js_output_folder):
        mkdir(js_output_folder)

    css_output_folder = join(this_folder, 'generator_output/css')
    if not exists(css_output_folder):
        mkdir(css_output_folder)

    # initialize template engine
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(join(this_folder, 'templates')),
        trim_blocks=True,
        lstrip_blocks=True)

    template = jinja_env.get_template('survey_html.j2')

    f = open(join(output_folder, "%s.html" % model.survey.name), 'w')
    f.write(template.render(survey=survey_object, datetime=now))

    js_template = jinja_env.get_template('survey_js.j2')

    f = open(join(js_output_folder, 'index.js'), 'w')
    f.write(js_template.render(survey=survey_object, datetime=now))

    copy(join(this_folder, 'templates/styles.css'), css_output_folder)
   
if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print('Error: Survey file is missing.')
    else:
        survey_file = sys.argv[1]
        generate(survey_file)
        