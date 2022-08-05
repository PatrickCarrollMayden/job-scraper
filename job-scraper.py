from fileinput import filename
import requests
from bs4 import BeautifulSoup
import pandas as pd

user_input = input('What job results would you like?')
search_params = user_input.split()

def get_search_term_and_translate():
    base_url = ''

    if len(search_params) > 1:
        for index, word in enumerate(search_params):
            if index+1 != len(search_params):
                base_url += word + "%20"
            else:
                base_url += word
    else:
        base_url += search_params[0]

    return base_url


def extract(page):
    base_url = get_search_term_and_translate()

    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    url = f'https://uk.indeed.com/jobs?q={base_url}&l=London%2C%20Greater%20London&start={page}&vjk=133a86ba2db9357c'

    response = requests.get(url, headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('table', class_ = 'jobCard_mainContent')
    for item in divs:
        title = item.find('a').text
        company = item.find('span', class_ = 'companyName').text
        
        try:
            salary = item.find('div', class_ = 'attribute_snippet').text
        except:
            salary = ''

        job = {
            'title': title,
            'company': company,
            'salary': salary
        }
        joblist.append(job)
    return

joblist = []

for i in range(0, 40, 10):    #looping through 4 pages worth
    print(f'Getting page, {i}')
    c = extract(0)
    transform(c)

df = pd.DataFrame(joblist)

filename = 'jobs.csv'

print(f'Exported to {filename}')

df.to_csv(filename)


