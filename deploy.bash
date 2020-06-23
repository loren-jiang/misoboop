#!/bin/bash
cd /home/loren/Documents/code_projects/django/misoboop;
source /home/loren/environments/misoboop_env/bin/activate;

pytest;

bash /home/loren/Documents/code_projects/django/misoboop/collect-compress.bash;

git push live master;

grep 'DO_SUDO_USER_PASSWORD=' .env | cut -d \=   -f2 | ssh -tt loren@165.227.9.4 "sudo supervisorctl restart live";