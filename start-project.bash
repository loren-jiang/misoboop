#!/bin/bash

cd ~/Documents/code_projects/django/misoboop;
source ~/environments/misoboop_env/bin/activate;
python manage.py test;
python manage.py runserver;
# gulp dj-runserver;
# gulp watch;
