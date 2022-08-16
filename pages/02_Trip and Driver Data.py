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



df_tripid = data.groupby(['TripID', 'Reference', 'DriverCode', 'TripType', 'AssetLabel', 'AssetStatus', 'CategoryName', 'CustomerName', 'DeviceType', 'Loaded', 'SiteName', 'TripSource', 'TripDestination', 'WaybillNumber', 'Latitude', 'Longitude']).agg({'Distance':'min', 'Distance2':'max', 'Odometer':'min', 'Odometer2':'max', 'DateTimeStarted':'min', 'DateTimeReceived':'max', 'AverageSatellites':'mean', 'AverageSpeed':'mean', 'MaxSpeed':'max'}).round(2)
df_tripid.reset_index(inplace=True)
df_tripid['Odometer Distance'] = df_tripid['Odometer2'] - df_tripid['Odometer']
df_tripid['GPS Distance'] = df_tripid['Distance2'] - df_tripid['Distance']
df_tripid['Duration'] = (df_tripid['DateTimeReceived'] - df_tripid['DateTimeStarted'])
source_destination_df = df_tripid.copy()


df_tripid = data.groupby(['TripID', 'Reference', 'DriverCode', 'TripType', 'AssetLabel', 'AssetStatus', 'CategoryName', 'CustomerName', 'DeviceType', 'Loaded', 'SiteName', 'TripSource', 'TripDestination', 'WaybillNumber']).agg({'Distance':'min', 'Distance2':'max', 'Odometer':'min', 'Odometer2':'max', 'DateTimeStarted':'min', 'DateTimeReceived':'max', 'AverageSatellites':'mean', 'AverageSpeed':'mean', 'MaxSpeed':'max'}).round(2)
df_tripid.reset_index(inplace=True)
df_tripid['Odometer Distance'] = df_tripid['Odometer2'] - df_tripid['Odometer']
df_tripid['GPS Distance'] = df_tripid['Distance2'] - df_tripid['Distance']
df_tripid['Duration'] = (df_tripid['DateTimeReceived'] - df_tripid['DateTimeStarted'])



df_tripid_distance_duration = df_tripid[['TripID', 'Reference', 'GPS Distance', 'Odometer Distance', 'Duration', 'AverageSatellites', 'AverageSpeed', 'MaxSpeed']]

df_tripid2 = data.groupby(['DriverCode', 'TripID', 'Reference', 'DateTimeReceived', 'TripType', 'AssetLabel', 'AssetStatus', 'CategoryName', 'Region', 'City', 'CustomerName', 'Longitude', 'Latitude', 'Loaded', 'NumSatellites', 'SiteName', 'TripDestination', 'TripSource', 'WaybillNumber', 'ActualSpeed']).agg({'Distance':'min', 'Distance2':'max', 'Odometer':'min', 'Odometer2':'max'})

df_tripid3 = df_tripid2.reset_index()
df_tripid4 = df_tripid3.merge(df_tripid_distance_duration, on=['TripID', 'Reference'], how='left')

#test = df_tripid4[df_tripid4['TripID'] == 3100182280]
#test = df_tripid4[df_tripid4['TripID'] == 9000257036]
#trip_df = df_tripid4[df_tripid4['TripID'] == 3100329545]
# df_tripid4.sort_values('DateTimeReceived', ascending=True, inplace=True)
# trip_df = df_tripid4.reset_index(drop=True)




df = df_tripid4



st.title('Trip and Driver Data')
       
    
#st.header('Select Parameters for Trip Analysis')

with st.sidebar:

    vehicle_select = st.multiselect('Choose the vehicles for analysis', sorted(list(df['AssetLabel'].unique())), ['HGV'])
    
    trip_type = st.multiselect('Choose the trip type for analysis', sorted(list(df['TripType'].unique())), [0, 1, 2])
        
        
    #with col3:
    load_status = st.multiselect('Choose if the vehicle is loaded or not', sorted(list(df['Loaded'].unique())), ['Yes', 'No'])
            
    status_select = st.multiselect('Choose the asset status for analysis', sorted(list(df['AssetStatus'].unique())), ['InService'])
      
    trip_source = st.multiselect('Choose the trip source analysis', sorted(list(df['TripSource'].unique())), ['DANGOTE MINE 2', 'STAGING AREA ', 'IBESE CEMENT PLANT', 'UNKNOWN'])
    
        


try:
    if not vehicle_select:
        st.error("Please select at least one vehicle type.")
    elif not trip_type:
        st.error("Please select at least one trip type.")
    elif not trip_source:
        st.error("Please select at least one trip source.")            
    elif not status_select:
        st.error("Please select an asset status.")                    
    elif not load_status:
        st.error("Please select load status.")       
    else: 
        df = df[df['AssetLabel'].isin(vehicle_select)]
        df = df[df['TripType'].isin(trip_type)]
        df = df[df['TripSource'].isin(trip_source)]
        df = df[df['AssetStatus'].isin(status_select)]
        df = df[df['Loaded'].isin(load_status)]
#            df = df[df['Loaded'].isin(loaded)]
except urllib.error.URLError as e:
    st.error("""
        **This demo requires internet access.**
        Connection error: %s
        """
        % e.reason)
             
            
            
        #& df['Salesperson'].isin(salesperson) & ~data1['Customer'].isin(customer) & ((data1['Invoice Payment Date'].dt.date > start_date) & (data1['Invoice Payment Date'].dt.date < end_date))]

#st.header('Selected Filter Trip and Driver Count')

col1, col2 = st.columns(2)
col1.metric(label='No. of Unique Trips', value='{}'.format(df['TripID'].nunique()))
col2.metric(label='No. of Unique Drivers', value=df['DriverCode'].nunique())
#col13.metric(label='Trip Duration', value='{}d-{}h-{}m'.format(cdays, chours, cminutes))
#col14.metric(label='Trip Maximum Speed', value='{}km/h'.format(plot_df['MaxSpeed'].max()))


col6, col7 = st.columns(2)

with col6:
    trip_choice = sorted(list(df['TripID'].unique()))
    choice_selected = st.selectbox('Trip ID Code', trip_choice)    
    

    plot_df = df[df['TripID']==choice_selected]

with col7:
    trip_choice = sorted(list(df['DriverCode'].unique()))
    choice_selected = st.selectbox('Driver Code', trip_choice)    

    plot_df = df[df['DriverCode']==choice_selected]




st.header('Selected Trip Statistics')    


ctd = plot_df['Duration'].max()
cdays = ctd.days
chours, cremainder = divmod(ctd.seconds, 3600)
cminutes, cseconds = divmod(cremainder, 60)
# If you want to take into account fractions of a second
cseconds += ctd.microseconds / 1e6



col11, col12, col13, col14 = st.columns(4)
col11.metric(label='Trip Odometer Distance', value='{}km'.format(plot_df['Odometer Distance'].max()))
col12.metric(label='Trip GPS Distance', value=plot_df['GPS Distance'].max())
col13.metric(label='Trip Duration', value='{}d-{}h-{}m'.format(cdays, chours, cminutes))
col14.metric(label='Trip Maximum Speed', value='{}km/h'.format(plot_df['MaxSpeed'].max()))



plot_df.sort_values('DateTimeReceived', ascending=True, inplace=True)
plot_df = plot_df.reset_index(drop=True)
    
    #loc = plot_df[['Latitude', 'Longitude']]
    
    #details = 'Dates: {} to {}, \nLoaded: {}, \nAsset Class: {}, \nAsset Status: {}, \nNo. of Satellites: {}, \nGPS Distance: {}, \nOdometer Distance: {}km \nDuration: {} \nSource: {} \nDestination: {}'.format(plot_df['DateTimeReceived'].min(), plot_df['DateTimeReceived'].max(), plot_df['Loaded'].iloc[0], plot_df['AssetLabel'].iloc[0], plot_df['AssetStatus'].iloc[0], plot_df['AverageSatellites'].iloc[0], plot_df['GPS Distance'].iloc[0], plot_df['Odometer Distance'].iloc[0], plot_df['Duration'].iloc[0], plot_df['TripSource'].iloc[0], plot_df['TripDestination'].iloc[0])
    
#    if 'maps2' in locals():
#        del map2
    
map2 = folium.Map(location=[9.169503, 8.111194], zoom_start=6)
    
marker_cluster = plugins.MarkerCluster().add_to(map2)

#popup_details = 'Index: {}, \nDate: {}, \nSatellites: {}, \nCity: {}'.format(test[test['DateTimeReceived']==
#                                                                                 row['DateTimeReceived']].index.values, row['DateTimeReceived'], row['NumSatellites'], row['City'])

colormap = cm.LinearColormap(colors=['red','lightblue'], index=[90,100],vmin=90,vmax=100)

#test['marker_color'] = pd.cut(test['DateTimeReceived'], bins=4, labels=['yellow', 'green', 'blue', 'red'])

for i, row in plot_df.iterrows():
    popup_details = 'Index: {}, \nDriverCode: {}, \nTripID: {}, \nDate: {}, \nStatus: {}, \nSpeed: {}, \nSatellites: {}, \nCity: {}'.format(plot_df[plot_df['DateTimeReceived']==                               row['DateTimeReceived']].index.values, row['DriverCode'], row['TripID'], row['DateTimeReceived'], row['AssetStatus'], row['ActualSpeed'], row['NumSatellites'], row['City'])
    
    folium.Marker(location=row[['Latitude','Longitude']].tolist(), color=colormap(i), cluster_marker=True, popup=popup_details).add_to(marker_cluster)


folium_static(map2, width=1000, height=600)