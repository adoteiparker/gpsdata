import streamlit as st

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
plt.rcParams.update({'font.size': 50})
import seaborn as sns


from matplotlib.cm import rainbow
import branca
import branca.colormap as cm


import datetime as dt
import urllib
from PIL import Image

import folium
from folium import plugins
#from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

import geopandas

data = st.session_state['data']


regions_gdf = st.session_state['regions_gdf']


    
regional_activity_df = data.groupby('Region')['DateTimeReceived'].count()
regional_activity_df = regional_activity_df.reset_index()
regional_activity_df = regional_activity_df.rename(columns={'DateTimeReceived':'Total Pings'})


region_satellite_df = data.groupby('Region')['NumSatellites'].mean()
region_satellite_df = region_satellite_df.reset_index()
region_satellite_df = region_satellite_df.rename(columns={'NumSatellites':'Average Satellite Coverage'})
regional_activity_df['Average Satellite Coverage'] = region_satellite_df['Average Satellite Coverage']

##### Trip Source and Destination Analysis

source_count = data.groupby('TripSource').agg({'Latitude':'mean', 'Longitude':'mean', 'DateTimeStarted':'count'})
source_count = source_count.reset_index()
source_count = source_count.rename(columns={'DateTimeStarted':'Count'})
source_df = source_count


destination_count = data.groupby('TripDestination').agg({'Latitude':'mean', 'Longitude':'mean', 'DateTimeReceived':'count'})
destination_count = destination_count.reset_index()
destination_count = destination_count.rename(columns={'DateTimeReceived':'Count'})
destination_df = destination_count

st.title('Satellite Data Analysis')


with st.sidebar:

    choice = ['Average Satellite Coverage', 'Total Pings', 'Source and Destination Analysis']
    choice_selected = st.selectbox('Select Choice', choice)





if choice_selected != 'Source and Destination Analysis':


    map2 = folium.Map(location=[9.169503, 8.111194], zoom_start=6)
    myscale = (regional_activity_df['Total Pings'].quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
    
    folium.GeoJson(data=regions_gdf['geometry']).add_to(map2)
    
    folium.Choropleth(
        geo_data=regions_gdf,
        name="choropleth",
        data=regional_activity_df,
        columns=["Region", choice_selected],
        nan_fill_color='white',
        nan_fill_opacity=0.75,
        key_on='feature.properties.admin1Name',
        threshold_scale=myscale if choice_selected=='Total Pings' else 7,
        popup = regional_activity_df.Region,
        fill_color="Reds" if choice_selected=='Total Pings' else 'Blues',
        fill_opacity=0.5,
        line_opacity=.1,
        legend_name=choice_selected,
    ).add_to(map2)
    
    folium.LayerControl().add_to(map2)
    
    #map2
    folium_static(map2, width=1000, height=600)    
else:

    map2 = folium.Map(location=[9.169503, 8.111194], zoom_start=6)

    for i in range(0,len(source_df)):
        folium.Circle(
          location=[source_df.iloc[i]['Latitude'], source_df.iloc[i]['Longitude']],
          popup='Source: {}, \nCount: {}'.format(source_df.iloc[i]['TripSource'],source_df.iloc[i]['Count']),
          radius=float(source_df.iloc[i]['Count'])*2,
          color='crimson',
          fill=True,
          fill_color='crimson'
       ).add_to(map2)
        
    for i in range(0,len(destination_df)):
        folium.Circle(
          location=[destination_df.iloc[i]['Latitude'], destination_df.iloc[i]['Longitude']],
          popup= 'Destination: {}, \nCount: {}'.format(destination_df.iloc[i]['TripDestination'],destination_df.iloc[i]['Count']),
          radius=float(destination_df.iloc[i]['Count'])*2,
          color='#69b3a2',
          fill=True,
          fill_color='#69b3a2'
       ).add_to(map2)
    
        
    folium_static(map2, width=1000, height=600)    
    
    col1, col2 = st.columns(2)
    
    with col1:
    
        st.dataframe(source_df)
        
    with col2:        
        st.dataframe(destination_df)        
    
