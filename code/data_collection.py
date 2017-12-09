"""
Scrape data on gym locations
"""

# imports
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# scrape basic-fit
URL = 'https://www.basic-fit.com/nl-nl/sportscholen'
SOUP = BeautifulSoup(requests.get(URL).content, 'lxml')
GYM_URL = list()
LINKS = SOUP.find_all('a')
for link in tqdm(LINKS):
    if link['href'].startswith('/nl-nl/sportscholen/'):
        GYM_URL.append('https://www.basic-fit.com' + link['href'])
GYM_URL = GYM_URL[3:-6]

ADDRESS = list()
for url in tqdm(GYM_URL):
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    address = soup.find_all('li', {'class': 'active'})
    for addr in address:
        ADDRESS.append(addr.text.strip())

BF = pd.DataFrame({'company': 'Basic-Fit',
                   'address': ADDRESS})

# scrape fit-for-free
URL = 'https://www.fitforfree.nl/clubs'
SOUP = BeautifulSoup(requests.get(URL).content, 'lxml')

STREET = [street.text.replace('  ', ' ').strip() for
          street in
          SOUP.find_all('span', {'itemprop': 'streetAddress'})]
LOCALITY = [locality.text.replace('  ', ' ').strip() for
            locality in
            SOUP.find_all('span', {'itemprop': 'addressLocality'})]

FFF = pd.DataFrame({'company': 'Fit For Free',
                    'address': [x[0] + ', ' + x[1] for x in list(zip(STREET, LOCALITY))]})

# merge dataframes
GYM = pd.concat([BF, FFF])

# save data to file
GYM.to_csv('data/gym_raw_test.csv', sep=';', index=False)
