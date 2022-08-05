import requests
from bs4 import BeautifulSoup

def extract(page):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    url = f'https://uk.indeed.com/jobs?q=python%20developer&l=London%2C%20Greater%20London&start={page}&vjk=133a86ba2db9357c'

    response = requests.get(url, headers)
    return response.status_code

print(extract(0))
