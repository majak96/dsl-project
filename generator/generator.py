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
   
   
if __name__ == "__main__":
    main()