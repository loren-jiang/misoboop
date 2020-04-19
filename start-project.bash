#!/bin/bash

cd ~/Documents/code_projects/django/misoboop;
source ~/environments/misoboop_env/bin/activate;
python manage.py test;
gulp dj-runserver;
gulp watch;
