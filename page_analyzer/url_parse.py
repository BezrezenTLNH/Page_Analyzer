import requests
from bs4 import BeautifulSoup


def url_parse(url):
    try:
        r = requests.get(url)
        r.raise_for_status()

    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException

    else:
        status_code = r.status_code
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.select_one('title')
        h1 = soup.select_one('h1')
        description = soup.select_one('meta[name="description"]')

    return status_code, h1, title, description
