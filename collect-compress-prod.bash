#!/bin/bash

cd ~/live;
source ~/bin/activate;

# use production settings needed for static file collection
export USE_PRODUCTION=true;

# collectstatic will push to s3
python manage.py collectstatic --no-input;
# django-compressor will handle versioning and push to s3
# output files are version controled for cache busting
python manage.py compress;
