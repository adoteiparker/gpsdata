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
    
    # asset_labels = {0:'Car', 1:'Van', 2:'HGV', 3:'PSV', 4:'Motor Cycle', 5:'Ambulance', 6:'4x4', 7:'Container', 8:'Trailer', 9:'Crane', 10:'Dump Truck', 11:'Fire Engine', 12:'Train', 13:'Mini Bus', 14:'Helicopter', 15:'Plane', 16:'Police Car', 17:'Trawler', 18:'Camper', 19:'Speed Boat', 20:'Ship', 21:'Farm Vehicle', 22:'Generator', 23:'Mobile Tower', 24:'Taxi', 25:'Dog', 26:'Cat', 27:'Pet Other', 28:'Human', 29:'Other Vehicle', 30:'Custom Image', 31:'Forklift', 32:'Construction Equipment', 33:'Bicycle', 34:'Cement Truck', 35:'Coal Truck', 36:'Recovery Truck', 37:'Truck Mounted Crane', 38:'Tow Truck', 39:'Fuel Tanker', 40:'Mixer Truck', 41:'Quad Bike', 42:'Truck', 43:'IoT', 44:'Truck Head', 45:'Backhoe Loader', 46:'Dozer', 47:'Excavator', 48:'Motor Grader', 49:'Polaris Ranger', 50:'Sheep Foot Roller', 51:'Vibratory Roller', 52:'Wheel Loader'}

    # df['AssetLabel'] = df['AssetClass'].apply(lambda x: asset_labels[x])
    # loaded_labels = {0:'No', 1:'Yes'}
    # df['Loaded'] = df['Load'].apply(lambda x: loaded_labels[x])

    # df['DriverCode'] = df['DriverCode'].str.replace("'", "")
    # df['DriverCode'] = df['DriverCode'].str.replace(".", "")
    # df['DriverCode'] = df['DriverCode'].str.replace("PE", "")
    # df['DriverCode'].fillna(0, inplace=True)
    # #df = df[df['DriverCode'] != 0]
    # df['DriverCode'] = df['DriverCode'].astype(int)
    
    # df['CustomerName'].fillna('INTERNAL', inplace=True)
    # df['WaybillNumber'].fillna(1, inplace=True)
    # df['TripSource'].fillna('UNKNOWN', inplace=True)
    # df['TripDestination'].fillna('UNKNOWN', inplace=True)
    # df['Geofence'].fillna('UNKNOWN', inplace=True)
    # df['City'].fillna('UNKNOWN', inplace=True)
    # df['Region'].fillna('UNKNOWN', inplace=True)
    
    rgdf = geopandas.read_file('Test.zip')

    return df, rgdf

#@st.cache
#def get_geodata():
#regions_gdf = geopandas.read_file('Test.zip')
    #return rgdf
data1, regions_gdf1 = get_data()
data, regions_gdf = data1.copy(), regions_gdf1.copy()
#regions_gdf = get_geodata()

    
regional_activity_df = data.groupby('Region')['DateTimeReceived'].count()
regional_activity_df = regional_activity_df.reset_index()
regional_activity_df = regional_activity_df.rename(columns={'DateTimeReceived':'Total Pings'})


region_satellite_df = data.groupby('Region')['NumSatellites'].mean()
region_satellite_df = region_satellite_df.reset_index()
region_satellite_df = region_satellite_df.rename(columns={'NumSatellites':'Average Satellite Coverage'})
regional_activity_df['Average Satellite Coverage'] = region_satellite_df['Average Satellite Coverage']


data['Odometer2'] = data['Odometer']
data['Distance2'] = data['Distance']
data['DateTimeStarted'] = data['DateTimeReceived']
data['DateTimeStarted2'] = data['DateTimeReceived']
data['NumSatellites2'] = data['NumSatellites']
data['ActualSpeed2'] = data['ActualSpeed']
data['ActualSpeed3'] = data['ActualSpeed']

data.rename(columns={'ActualSpeed2':'AverageSpeed', 'ActualSpeed3':'MaxSpeed', 'NumSatellites2':'AverageSatellites'}, inplace=True)


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


##### Trip Source and Destination Analysis

source_count = source_destination_df.groupby('TripSource').agg({'Latitude':'mean', 'Longitude':'mean', 'DateTimeStarted':'count'})
source_count = source_count.reset_index()
source_count = source_count.rename(columns={'DateTimeStarted':'Count'})


destination_count = source_destination_df.groupby('TripDestination').agg({'Latitude':'mean', 'Longitude':'mean', 'DateTimeReceived':'count'})
destination_count = destination_count.reset_index()
destination_count = destination_count.rename(columns={'DateTimeReceived':'Count'})





def home(dataframe):
    
    st.title('Home')
    
    st.write('Testing')
    return


def data_stats(dataframe):
    
    st.header('Data Header')    
    st.write(data.head())
    
    st.header('Data Statistics')    
    st.write(data.describe())
    return


    

def satellite_plots(dataframe, dataframe1, dataframe2):
    
    regional_activity_df, source_df, destination_df = dataframe, dataframe1, dataframe2

    st.title('Satellite Data Analysis')
    

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
        
    return
        
        
# def source_destination_analysis(dataframe1, dataframe2):
    
#     st.title('Source and Destination Analysis')    
    
#     source_df = dataframe1
#     destination_df = dataframe2
    
    
#     map2 = folium.Map(location=[9.169503, 8.111194], zoom_start=6)

#     for i in range(0,len(source_df)):
#         folium.Circle(
#           location=[source_df.iloc[i]['Latitude'], source_df.iloc[i]['Longitude']],
#           popup='Source: {}, \nCount: {}'.format(source_df.iloc[i]['TripSource'],source_df.iloc[i]['Count']),
#           radius=float(source_df.iloc[i]['Count'])*2,
#           color='crimson',
#           fill=True,
#           fill_color='crimson'
#        ).add_to(map2)
        
#     for i in range(0,len(destination_df)):
#         folium.Circle(
#           location=[destination_df.iloc[i]['Latitude'], destination_df.iloc[i]['Longitude']],
#           popup= 'Destination: {}, \nCount: {}'.format(destination_df.iloc[i]['TripDestination'],destination_df.iloc[i]['Count']),
#           radius=float(destination_df.iloc[i]['Count'])*2,
#           color='#69b3a2',
#           fill=True,
#           fill_color='#69b3a2'
#        ).add_to(map2)
    
        
#     folium_static(map2, width=1000, height=600)    
    
#     col1, col2 = st.columns(2)
    
#     with col1:
    
#         st.dataframe(source_df)
        
#     with col2:        
#         st.dataframe(destination_df)
      
#     return
    


def trip_analysis(dataframe):
    
    st.title('Trip and Driver Data')
    
    df = dataframe.copy()
    #df = df[df['AssetStatus']=='InService']
    
    
    # st.header('Database Trip Statistics')
    
    
    # td = df['Duration'].max()
    # days = td.days
    # hours, remainder = divmod(td.seconds, 3600)
    # minutes, seconds = divmod(remainder, 60)
    # # If you want to take into account fractions of a second
    # seconds += td.microseconds / 1e6
    
    # col1, col2, col3, col4 = st.columns(4)
    # col1.metric(label='Maximum Odometer Distance for all Trips', value='{}km'.format(df['Odometer Distance'].max()))
    # col2.metric(label='Maximum GPS Distance for all Trips', value=df['GPS Distance'].max())
    # col3.metric(label='Maximum Trip Duration for all Trips', value='{}d-{}h-{}m'.format(days, hours, minutes))
    # col4.metric(label='Maximum Speed for all Trips', value='{}km/h'.format(df['MaxSpeed'].max()))
    
    st.header('Select Parameters for Trip Analysis')

    col1, col2, col3 = st.columns(3)    
    #col1, col2, col3, col4 = st.columns(4)
    
    with col1:    
        vehicle_select = st.multiselect('Choose the vehicles for analysis', sorted(list(df['AssetLabel'].unique())), ['HGV'])
    
    with col2:        
        trip_type = st.multiselect('Choose the trip type for analysis', sorted(list(df['TripType'].unique())), [0, 1, 2])
        
        
    with col3:
        load_status = st.multiselect('Choose if the vehicle is loaded or not', sorted(list(df['Loaded'].unique())), ['Yes', 'No'])
        
        
        
        
    col4, col5 = st.columns(2)
    #col1, col2, col3, col4 = st.columns(4)
    
    with col4:    
        status_select = st.multiselect('Choose the asset status for analysis', sorted(list(df['AssetStatus'].unique())), ['InService'])
    
    with col5:        
        trip_source = st.multiselect('Choose the trip source analysis', sorted(list(df['TripSource'].unique())), ['DANGOTE MINE 2', 'STAGING AREA ', 'IBESE CEMENT PLANT', 'UNKNOWN'])
        
        
#    with col6:
#        trip_source = st.multiselect('Choose the trip source analysis', sorted(list(df['TripSource'].unique())), ['DANGOTE MINE 2'])        
        
#    with col4:        
#        loaded = st.selectbox('Choose if the vehicles are loaded',  sorted(list(df['Loaded'].unique())), ['Yes'])
#        loaded = st.selectbox('Choose if the vehicles are loaded', list(df['Loaded'].unique()), ['Yes'])
        
    
    # loaded = st.selectbox('Choose loaded or unloaded for analysis', sorted(list(df['Loaded'].unique())), ['Yes'])


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
    
    st.header('Selected Filter Trip and Driver Count')
    
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

    return

    
    
    
    
    
    
    
    

    # journal = st.multiselect('Choose the journals for analysis', sorted(list(data1['Journal'].unique())), ['Bank (GHS)'])
    # customer = st.multiselect('Choose the customers to not include', sorted(list(data1['Customer'].unique())), ['Parker Pharmacy - Korle Bu'])    


#st.title('Transportation Analysis')
#st.text('This is a web app to explore various metrics from the transportation data')


st.sidebar.title('Transportation Analysis')
st.sidebar.header('Navigation')
page_options = st.sidebar.radio('Pages', options=['Satellite Data', 'Trip and Driver Data', 'Data Statistics'])

#if page_options == 'Home':
#    home(data)
if page_options == 'Data Statistics':
    data_stats(data)
elif page_options == 'Satellite Data':
    satellite_plots(regional_activity_df, source_count, destination_count)
#elif page_options == 'Source and Destination Analysis':
#    source_destination_analysis(source_count, destination_count)
elif page_options == 'Trip and Driver Data':
    trip_analysis(df_tripid4)




# st.header('Data Statistics')
# st.write(data.describe())





#analysis = st.container()


    
    
# with analysis:





