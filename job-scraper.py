from fileinput import filename
import requests
from bs4 import BeautifulSoup
import pandas as pd

filename = 'jobs.csv'

user_input = input('What job results would you like?')
search_params = user_input.split()

location_input = input('What location?')
location_params = location_input.split()

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

def get_search_location():
    location = ''

    if len(location_params) > 1:
        for index, word in enumerate(location_params):
            if index+1 != len(location_params):
                location += word + "%20"
            else:
                location += word
    else:
        location += location_params[0]

    return location


def extract(page):
    base_url = get_search_term_and_translate()
    location = get_search_location()

    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    url = f'https://uk.indeed.com/jobs?q={base_url}&l={location}&start={page}'

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

for i in range(0, 60, 15):    #looping through 4 pages worth
    print(f'Getting page, {i}')
    c = extract(0)
    transform(c)

df = pd.DataFrame(joblist)
df = df.drop_duplicates(subset=None, keep="first", inplace=False)

print(f'Exported to {filename}')

df.to_csv(filename)


