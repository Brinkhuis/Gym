"""
Plot data on Google Maps
"""

# imports
import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import (GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d,
                          PanTool, WheelZoomTool, BoxSelectTool, HoverTool)

# read data
GYM = pd.read_csv('data/gym.csv', sep=';')

# add color per company
GYM['color'] = GYM['company'].apply(lambda x: 'red' if x == 'Fit For Free' else 'blue')

# For GMaps to function, Google requires you obtain and enable an API key:
#
#     https://developers.google.com/maps/documentation/javascript/get-api-key
#
# Replace the value below with your personal API key:

API_KEY = '-- Replace this value with your personal API key --'

MAP_CENTER_LAT = (max(GYM['latitude']) + min(GYM['latitude'])) / 2
MAP_CENTER_LNG = (max(GYM['longitude']) + min(GYM['longitude'])) / 2
MAP_OPTIONS = GMapOptions(lat=MAP_CENTER_LAT, lng=MAP_CENTER_LNG, map_type='roadmap', zoom=8)

PLOT = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=MAP_OPTIONS)
PLOT.api_key = API_KEY
SOURCE = ColumnDataSource(data=dict(lat=GYM['latitude'], lng=GYM['longitude'], addr=GYM['address'],
                                    col=GYM['color'], company=GYM['company']))
CIRCLE = Circle(x='lng', y='lat', size=15, fill_color='col', fill_alpha=0.6, line_color=None)
PLOT.add_glyph(SOURCE, CIRCLE)
PLOT.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(), HoverTool())
HOVER = PLOT.select_one(HoverTool)
HOVER.tooltips = [('Company', '@company'), ('Address', '@addr'),
                  ('Latitude, Longitute', '(@lat, @lng)')]
output_file('plots/gym.html')
show(PLOT)
