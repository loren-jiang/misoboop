"""
Django settings for misoboop project, which defaults to
settings_dev.py OR settings_prod.py (development vs production)
"""
import os

# Delegate which settings to use

if os.environ.get('DJANGO_SETTINGS_MODE')=="dev" and not os.environ.get('USE_PRODUCTION'):
    # print('Development settings used.')
    from misoboop.settings_dev import *
elif os.environ.get('DJANGO_SETTINGS_MODE')=="test" and not os.environ.get('USE_PRODUCTION'):
    # print('Test setting used.')
    from misoboop.settings_test import *
else:
    # print('Production settings used.')
    from misoboop.settings_prod import *
