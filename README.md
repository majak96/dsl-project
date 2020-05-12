# SurveyIT

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

## Description

SurveyIT is a domain-specific language for definining web-based surveys. SurveyIT enables defining surveys using built-in question types, as well as defining new question types. Surveys are generated as HTML, CSS and JavaScript files. 

Supported built-in question types:
- Text question
- Number question
- Choice question
- Drop down question
- Linear scale question
- Date question
- Time question
- Likert scale question

SurveyIT is created for the purpose of the Domain-Specific Languages course at the Faculty of Technical Sciences, University of Novi Sad.

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
2. Change the current working directory (assuming you are positioned in the directory of the cloned repository)
```
$ cd generator
```
3. Generate your survey
```
$ python generator.py example.srvy
```
If the generation process completes successfully, generated survey files are located in the generator_output folder.

## Technologies used
- Python 3.6+
- [textX](https://github.com/textX/textX)
- Jinja2 template engine

## Contributors

- [Marijana Matkovski](https://github.com/matkovskim)  
- [Marijana Kološnjaji](https://github.com/majak96)  
- [Vesna Milić](https://github.com/vesnamilic)  
