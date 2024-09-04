from urllib.parse import urlparse
from validators import url as is_url_valid


def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_url = f'{parsed_url.scheme}://{parsed_url.hostname}'
    return normalized_url


def validate(url):
    if not url:
        return 'URL обязателен для заполнения'
    if len(url) > 255:
        return 'Введенный URL превышает длину в 255 символов'
    if not is_url_valid(url):
        return 'Некорректный URL'
