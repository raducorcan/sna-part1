import urllib3
from bs4 import BeautifulSoup


def create_soup_from_url(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    soup = BeautifulSoup(r.data, 'html.parser')
    return soup
