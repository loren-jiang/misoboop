"""
Django test settings for misoboop project.
"""
from .settings_prod import *
import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
