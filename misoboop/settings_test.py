import os 

DATABASES = {
    "default": os.getenv("DATABASE_URL", default="postgres://postgres:@localhost/circle_test")
}

DATABASES["default"]["ATOMIC_REQUESTS"] = True