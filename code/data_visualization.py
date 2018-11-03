"""
Plot data on a map
"""

# import modules
import pandas as pd
import folium# pip install folium
from folium.plugins import MarkerCluster

# read data
gym = pd.read_csv('data/gym_geo.csv', sep=';')

# dict of dicts for gym attributes
attribs = {'Basic-Fit'   : {'url': 'www.basic-fit.com',
                            'icon_url': 'http://res.cloudinary.com/brinkhuis/image/upload/v1512746206/basicfit_wexzjg.png',
                            'icon_size': (84, 28)}, 
           'Fit For Free': {'url': 'https://www.fitforfree.nl',
                            'icon_url': 'http://res.cloudinary.com/brinkhuis/image/upload/v1512745660/fitforfree_wo2t4c.png',
                            'icon_size': (42, 42)}}

# create map
m = folium.Map(location=[52.07, 5.12], zoom_start=12, tiles='Stamen Terrain')

# marker cluster
marker_cluster = MarkerCluster().add_to(m)

# add markers
for i in range(gym.shape[0]):
    folium.Marker([gym.iloc[i].y, gym.iloc[i].x],
                  icon=folium.features.CustomIcon(attribs[gym.iloc[i].company]['icon_url'],
                                                  icon_size=attribs[gym.iloc[i].company]['icon_size']),
                  popup='<b>' + gym.iloc[i].company.upper() + '</b><br>'
                  + '<i>'+ gym.iloc[i].address.split(', ')[0] + '</i><br>'
                  + '<i>' + gym.iloc[i].address.split(', ')[1] + '</i><br>'
                  + '<a href={0} target="_blank"</a>{0}'.format(attribs[gym.iloc[i].company]['url'])).add_to(marker_cluster)

# save map
m.save('plots/gym_map.html')
