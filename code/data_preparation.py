"""
Data preparation
"""

# imports
import pandas as pd
import geocoder
import re

# read data
df = pd.read_csv('data/gym_raw.csv', sep=';')

# correct data
df.loc[df['address'] == 'Stadionplein (ingang 18) 2, 5616RX EINDHOVEN', ['address']] = 'Stadionplein 2, 5616RX EINDHOVEN'
df.loc[df['address'] == 'Bislet 11, 7825SB EMMEN', ['address']] = 'Bislett 11, 7825SB EMMEN'
df.loc[df['address'] == 'Antillenstraat 7 E-H, 9714JT GRONINGEN', ['address']] = 'Antillenstraat 7E, 9714JT GRONINGEN'
df.loc[df['address'] == 'Zwaagdijk 467A, 1689PC HOORN', ['address']] = 'Zwaagdijk 467A, 1689PC ZWAAG'
df.loc[df['address'] == 'C. van der Doesstraat 22 1e Etage, 1972AT IJMUIDEN', ['address']] = 'C. van der Doesstraat 22, 1972AT IJMUIDEN'
df.loc[df['address'] == 'Martin Luther Kingweg 205-207, 1504DG ZAANDAM', ['address']] = 'Dominee Martin Luther Kingweg 205, 1504DG ZAANDAM'
df.loc[df['address'] == 'Menno Simonszplein 22, Haarlem', ['address']] = 'Menno Simonszweg 22, Haarlem'

# add columns for latitude and longitude
df['x'] = None
df['y'] = None

# helper function
def verwijder_postcode(adres):
    pattern = '[0-9][0-9][0-9][0-9][A-Z][A-Z]'
    fa = re.findall(pattern, adres)
    if len(fa) != 0:
        i = adres.find(fa[0])
        j = i + 7
        nieuw_adres = f'{adres[:i]}{adres[j:]}'
    else:
        nieuw_adres = adres
    return nieuw_adres

# get latitude and longitude 
for index, row in df.iterrows():
    try:
        a = verwijder_postcode(row.address)
        g = geocoder.osm(a).osm
        df.loc[index, ['x']] = g['x']
        df.loc[index, ['y']] = g['y']
    except:
        pass

# save data
file_name = 'data/gym_geo.csv'
df.to_csv(file_name, sep=';', index=False)
print(f'Data saved to {file_name}')
