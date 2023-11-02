import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from validators import url as valid


def url_normalize(url):
    url = urlparse(url)
    return f'{url.scheme.lower()}://{url.netloc.lower()}'


def url_validate(url):
    if len(url) < 255 and valid(url):
        return True


def url_parse(url):

    page_data = {}

    try:
        r = requests.get(url)
        r.raise_for_status()

    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException

    else:
        page_data['status_code'] = r.status_code
        soup = BeautifulSoup(r.text, 'html.parser')
        page_data['title'] = soup.select_one('title')
        page_data['h1'] = soup.select_one('h1')
        page_data['description'] = soup.select_one('meta[name="description"]')

    return page_data