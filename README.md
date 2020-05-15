# SurveyIT

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

## Description

SurveyIT is a domain-specific language for definining web-based surveys. The language is created for the purpose of the Domain-Specific Languages course at the Faculty of Technical Sciences, University of Novi Sad.

SurveyIT enables defining surveys using built-in question types:

- Text question
- Number question
- Choice question
- Drop down question
- Linear scale question
- Date question
- Time question
- Likert scale question

SurveyIT also includes a sublanguage for defining new question types. In order to use the new user-defined question type, a Jinja2 template for the question type must be provided.

Surveys are generated as HTML, CSS and JavaScript files. 

## Example
This is a short example of a survey defined using SurveyIT, including a user-defined question type EmailQuestion. Full example is available in the generator folder of the repository.
```
question_type EmailQuestion {
    description: "Question type with the special email input field"
    parameters {
        string placeholder
    }
}

survey SoftwareEvaluation {

    title : "Software evaluation"
    description: "Description of this awesome survey"
    author: "Tim 3"

    submit_url:"https://exampleURL.com"

    success_message: "You have successfully submitted your answers! Thank you for participating."
    error_message: "Unfortunately, an error occured. Please try again."

    section {
        title: "General information"

        @Required
        @TextQuestion
        question Question0 {
            title: "Name"
            multiline: false
        } 

        @Required
        @EmailQuestion
        question Question1 {
            title: "Email address"
            placeholder: "Insert your email address"
        }

        @Required
        @ChoiceQuestion
        question Question2 {
            title: "How did you find out about this software?"
            choices: ["From a friend", "From a family member", "From a website", "Other"]
            multiple: true
        }
    }

    section {
        title: "Software evaluation" 

        @Required
        @LikertScaleQuestion
        question Question3 {
            title: "How satisfied are you with:"
            rows_names: ["The reliability of this software", 
                         "The security of this software", 
                         "The software's ease of use",
                         "The look and feel of this software"]
            columns_names: ["Not satisfied at all", "Not so satisfied", "Somewhat satisfied", "Very satisfied", "Extremely satisfied"]
            multiple_in_row: false
        }

        @LinearScaleQuestion
        question Question4 {
            title: "How likely is it that you would recommend this software to a friend or a family member?"
            min_value: 0
            max_value: 5
            min_description: "not at all likely"
            max_description: "extremely likely"
        } 

        @Required
        @DropDownQuestion
        question Question5 {
            title: "Do you plan to continue using this software?"
            options: ["Yes", "No", "I'm not sure"]
        }
    }
}
```

## Instructions
1. Install requirements
```
$ pip install -r requirements.txt
```
2. Generate your survey
```
$ textx generate example_survey.srvy --target html+css+js
```
Use flag ```-o``` or ```--output-path``` to provide the output path for generated files. If output path is not provided, files will be generated in the directory of the input file.

Use flag ```--overwrite``` to overwrite the target files if they already exist.

If the generation process completes successfully, generated survey files will be located in the generator_output folder in the provided output path or the directory of the input file.

## Technologies used
- Python 3.6+
- [textX](https://github.com/textX/textX)
- Jinja2 template engine

## Contributors

- [Marijana Matkovski](https://github.com/matkovskim)  
- [Marijana Kološnjaji](https://github.com/majak96)  
- [Vesna Milić](https://github.com/vesnamilic)  
