from urllib.parse import urlparse, urljoin, urlencode


class UrlBuilder:
    def __init__(self, base_url: str, path: str, query: dict):
        self._base_url = base_url
        self._path = path
        self._query = query

    @property
    def query(self):
        return self._query

    @property
    def base_url(self):
        return self._base_url

    @property
    def path(self):
        return self._path

    @property
    def url(self) -> str:
        url = urlparse(urljoin(self._base_url, self._path))
        url = url._replace(query=urlencode(self._query))
        return url.geturl()
