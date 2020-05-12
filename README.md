# SurveyIT

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

## Description

SurveyIT is a domain-specific language for definining web-based surveys. SurveyIT enables defining surveys using built-in question types, as well as defining new question types. Surveys are generated as HTML, CSS and JavaScript files. 

SurveyIT is created for the purpose of the Domain-Specific Languages course at the Faculty of Technical Sciences, University of Novi Sad.

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
