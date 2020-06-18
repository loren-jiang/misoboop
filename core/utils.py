import re
from bs4 import BeautifulSoup
from django.conf import settings

def remove_backslash_escaped(text):
    """Remove linebreaks (\n), tabs (\t), etc from string"""
    return re.sub('\s+', ' ', text)


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def lazify_images(html, lazy_class=settings.LAZIFY_IMAGE_CLASS):
    soup = BeautifulSoup(html, 'html.parser')
    soup_imgs = soup.find_all('img')
    for img in soup_imgs:
        img['class'] = lazy_class
        img['data-src'] = img['src']
        del img['src']
    return str(soup.prettify())