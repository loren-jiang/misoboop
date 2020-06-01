import re
from bs4 import BeautifulSoup


def remove_backslash_escaped(text):
    """Remove linebreaks (\n), tabs (\t), etc from string"""
    return re.sub('\s+', ' ', text)


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def lozad_lazify_imgs(html):
    soup = BeautifulSoup(html, 'html.parser')
    soup_imgs = soup.find_all('img')
    for img in soup_imgs:
        img['class'] = 'lozad'
        img['data-src'] = img['src']
        del img['src']
    return str(soup.prettify())