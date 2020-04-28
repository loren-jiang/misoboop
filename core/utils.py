import re

def remove_backslash_escaped(text):
    """Remove linebreaks (\n), tabs (\t), etc from string"""
    return re.sub('\s+', ' ', text)

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

