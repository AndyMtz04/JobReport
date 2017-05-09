# JobReport
Jobreport utilizes BeautifulSoup 4 to scrape jobs from job sites and pushbullet to send a message. 

# About JobReport
This project was inspired by a craigslist job scraping script, and at one point contained some of the same code.
Since then, the script has been completely redone and has implemented new features. 

# Setup

Install Python 3

Install Postgresql

For Linux, install, with a package manager, postgresql-devel and python-devel

Install with pip BeautifulSoup 4, requests, sqlalchemy, and pushbullet.py

Use template/template_main.py as a template and place it in JobReport/ directory

Use template/template_log_config.json as a template and place it in JobReport/ directory 

Use template/template_models.py as a empalte and place it in JobReport/job/ directory

Update the constants in template_main.py with the appropriate settings

Update the constant in job/template_models.py with the database URI

run template_main.py script

# Example
![Alt text](https://github.com/AndyMtz04/jobreporter/blob/master/images/soup_arguments.png)

In templates/template_main.py, craigslist job posting area is used to demonstrate the script.

Bs4 navigates through the black and red rectangles to scrape job links. 

* Black contains "element_1" with "ul" and "class_1" with "rows"

* Red contains "element_2" with "p" and "class_2" with "result-info"

* Green is handled by the JobReport instance.

````  
soup_args = {"element_1": "ul", "class_1": "rows", "id_1": None, "element_2": "p",
             "class_2": "result-info", "title_position": 0}
````

# ToDo
* Add tests

