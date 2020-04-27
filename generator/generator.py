from os import mkdir
from os.path import exists, dirname, join
from shutil import copy
import jinja2
from entities import Survey, Section, Question
from meta_model import get_metamodel

def main():
    
    this_folder = dirname(__file__)

    metamodel = get_metamodel()

    # build model
    model = metamodel.model_from_file(join(this_folder, 'example.srvy'))

    survey_name = model.survey.name
    survey_information = model.survey.survey_info
    survey_object = Survey(survey_name,
                           survey_information.title,
                           survey_information.description,
                           survey_information.author)

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

    # create output folder
    output_folder = join(this_folder, 'generator_output')
    if not exists(output_folder):
        mkdir(output_folder)

    # initialize template engine
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(join(this_folder, 'templates')),
        trim_blocks=True,
        lstrip_blocks=True)

    template = jinja_env.get_template('survey.j2')

    f = open(join(output_folder, "%s.html" % model.survey.name), 'w')
    f.write(template.render(survey=survey_object))

    copy(join(this_folder, 'templates/styles.css'), output_folder)
   
   
if __name__ == "__main__":
    main()