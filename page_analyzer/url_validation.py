from urllib.parse import urlparse
from validators import url as valid


def url_normalize(url):
    url = urlparse(url)
    return f'{url.scheme.lower()}://{url.netloc.lower()}'


def url_validate(url):
    if len(url) < 255 and valid(url):
        return True
