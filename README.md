# StackOverflow-Assignment

This project is an assignment as a part of an interview process. The goal of the project
is to make request to StackOverflow Questins API and display their results while maintaining 
page caching and limiting sessions requests according to given criteria.

## Installation Steps

1. Inside the project folder run the following command to install requirements
> pip install -r requirements.txt
2. Run the following to make migrations
> python manage.py makemigrations
3. Run the following to apply migrations
> python manage.py migrate
4. Run the following to run server
> python manage.py runserver