import re
import requests
from bs4 import BeautifulSoup
import nltk

MERCURY_API = 'https://mercury.postlight.com/parser?url='
api_key = "w2K2KogZrhKJpK9Z8KxaT9yaZ52uG9zgNMZk49Ut"

class ParserAPI(object):
    def __init__(self, api_key):
        super(ParserAPI, self).__init__()
        self.api_key = api_key
        self._session = requests.Session()

    def parse(self, url):
        url = '{0}{1}'.format(MERCURY_API, url)
        headers = {'x-api-key': self.api_key}

        r = self._session.get(url, headers=headers)

        return r.text

s = ParserAPI(api_key)
print(s.parse("http://docs.python-requests.org/en/master/user/advanced/"))