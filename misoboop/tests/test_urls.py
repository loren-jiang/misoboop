from django.conf import settings

URL_NAMES = []
def load_url_pattern_names(patterns):
    """Retrieve a list of urlpattern names"""
    global URL_NAMES
    for pat in patterns:
        if pat.__class__.__name__ == 'URLResolver':            # load patterns from this RegexURLResolver
            load_url_pattern_names(pat.url_patterns)
        elif pat.__class__.__name__ == 'URLPattern':           # load name from this RegexURLPattern
            if pat.name is not None and pat.name not in URL_NAMES:
                URL_NAMES.append( pat.name)
    return URL_NAMES

root_urlconf = __import__(settings.ROOT_URLCONF)        # access the root urls.py file
# print(load_url_pattern_names(root_urlconf.urls.urlpatterns))   # access the "urlpatterns" from the ROOT_URLCONF