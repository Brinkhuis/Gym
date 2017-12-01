"""
Data preparation
"""

# imports
import pandas as pd
import requests

# functions
def latlong(dataframe, address, latitude, longitude):
    """
    Function for finding and storing latitude and longitude for a given address
    dataframe: pandas DataFrame containing addresses
    address: name of the column in the DataFrame containing the addresses
    latitude: name of the column to store latitude
    longitude: name of the column to stor longitude
    """
    while dataframe.isnull().values.any():
        no_latlong_count_start = dataframe.loc[dataframe[latitude].isnull() |
                                               dataframe[longitude].isnull()].shape[0]
        for index, row in dataframe.iterrows():
            if pd.isnull(row[latitude]) or pd.isnull(row[longitude]):
                url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
                url = url + row[address].replace(' ', '+')
                response = requests.get(url)
                resp_json_payload = response.json()
                if len(resp_json_payload['results']) != 0:
                    dataframe.loc[index, longitude] = resp_json_payload['results'][0]['geometry']['location']['lng']
                    dataframe.loc[index, latitude] = resp_json_payload['results'][0]['geometry']['location']['lat']
        no_latlong_count_end = dataframe.loc[dataframe[latitude].isnull() | dataframe[longitude].isnull()].shape[0]
        if no_latlong_count_start == no_latlong_count_end:
            break

def validate():
    """
    Helper function to print message when latitudes and longitudes are found
    for all provided addressed or print addresses to be modified.
    """
    if GYM.loc[GYM['latitude'].isnull() | GYM['longitude'].isnull()].shape[0] == 0:
        print('Congrates, no missing latitudes or longitudes!')
    else:
        print(GYM.loc[GYM['latitude'].isnull() | GYM['longitude'].isnull()].address)

# read data
GYM = pd.read_csv('data/gym_raw.csv', sep=';')

# add columns for storing latitude and longitude
GYM['latitude'] = None
GYM['longitude'] = None

# get latitude and longitude
latlong(GYM, 'address', 'latitude', 'longitude')

# save data
GYM.to_csv('data/gym_geo.csv', sep=';', index=False)

# validate data
validate()

# modify data
GYM.loc[GYM['address'] == 'Stadionplein (ingang 18) 2, 5616RX EINDHOVEN', ['address']] = 'Stadionplein 2, 5616RX EINDHOVEN'

# get latitude and longitude
latlong(GYM, 'address', 'latitude', 'longitude')

validate()
# validate data

GYM.to_csv('data/gym.csv', sep=';', index=False)
