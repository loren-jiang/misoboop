"""
Django settings for misoboop project, which defaults to
settings_dev.py OR settings_prod.py (development vs production)
"""
import os

# Override production variables if DJANGO_DEVELOPMENT env variable is set
# and USE_PRODUCTION env variable is not set
if os.environ.get('DJANGO_DEVELOPMENT') and not os.environ.get('USE_PRODUCTION'):
    # print('Development settings used.')
    from misoboop.settings_dev import *
else:
    # print('Production settings used.')
    from misoboop.settings_prod import *
