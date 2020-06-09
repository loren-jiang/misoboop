#!/bin/bash
pytest;

bash /home/loren/Documents/code_projects/django/misoboop/collect-compress.bash;

git push live master;