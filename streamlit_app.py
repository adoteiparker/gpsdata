#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 01:36:54 2022

@author: adotei
"""

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

st.set_page_config(layout='wide')

@st.cache
def get_data():
    
#    df = pd.read_excel('historical-livePosition-data.xlsx', sheet_name='Sheet 1')
    df = pd.read_excel('data/Cleaned.xlsx', sheet_name='Sheet1')
    
    df.drop_duplicates(inplace=True)
       
    rgdf = geopandas.read_file('Nigeria_Shape.zip')

    return df, rgdf


data, regions_gdf = get_data()



data['Odometer2'] = data['Odometer']
data['Distance2'] = data['Distance']
data['DateTimeStarted'] = data['DateTimeReceived']
data['DateTimeStarted2'] = data['DateTimeReceived']
data['NumSatellites2'] = data['NumSatellites']
data['ActualSpeed2'] = data['ActualSpeed']
data['ActualSpeed3'] = data['ActualSpeed']

data.rename(columns={'ActualSpeed2':'AverageSpeed', 'ActualSpeed3':'MaxSpeed', 'NumSatellites2':'AverageSatellites'}, inplace=True)


st.session_state['data'] = data
st.session_state['regions_gdf'] = regions_gdf




st.sidebar.title('Transportation Analysis')
st.sidebar.header('Navigation')







