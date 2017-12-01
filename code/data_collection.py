"""
Scrape data on gym locations
"""

# imports
import pandas as pd
import requests
from bs4 import BeautifulSoup

# scrape basic-fit
URL = 'https://www.basic-fit.com/nl-nl/sportscholen'
SOUP = BeautifulSoup(requests.get(URL).text, 'html.parser')
GYM_URL = list()
LINKS = SOUP.find_all('a')
for link in LINKS:
    if link['href'].startswith('/nl-nl/sportscholen/'):
        GYM_URL.append('https://www.basic-fit.com' + link['href'])
GYM_URL = GYM_URL[3:-6]

ADDRESS = list()
for url in GYM_URL:
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    address = soup.find_all('li', {'class': 'active'})
    for addr in address:
        ADDRESS.append(addr.text.strip())

BF = pd.DataFrame({'company': 'Basic-Fit',
                   'address': ADDRESS})

# scrape fit-for-free
URL = 'https://www.fitforfree.nl/clubs'
SOUP = BeautifulSoup(requests.get(URL).text, 'html.parser')
SOUP.find_all('span', {'itemprop': ['streetAddress', 'addressLocality']})

STREET = list()
for address in SOUP.find_all('span', {'itemprop': 'streetAddress'}):
    STREET.append(address.text.replace('  ', ' ').strip())

LOCALITY = list()
for address in SOUP.find_all('span', {'itemprop': 'addressLocality'}):
    LOCALITY.append(address.text.replace('  ', ' ').strip())

FFF = pd.DataFrame({'company': 'Fit For Free',
                    'address': [x[0] + ', ' + x[1] for x in list(zip(STREET, LOCALITY))]})

# merge dataframes
GYM = pd.concat([BF, FFF])

# save data to file
GYM.to_csv('data/gym_raw.csv', sep=';', index=False)
