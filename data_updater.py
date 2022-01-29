import pandas as pd
import numpy as np
import streamlit as st
import requests
import json
import time
from datetime import datetime
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

def JSON_Downloader():
	offset=10
	limit=10
	#Get Total Number of records and First set of records
#	status.write("Getting Total Number of records and First set of records")
	JSONContent = requests.get("https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69?api-key=579b464db66ec23bdd000001fac7277b9e444f4f5c1abfd7d2dc9105&format=json&offset=0&limit=10").json()
	total=JSONContent['total']
#	my_bar.progress(offset/total)
#	status.write("Downloading "+str(offset)+ " of " + str(total) + " records")
	#Build JSON file by Downloading Total no. of records.
	while offset<total:
		JSONContent1 = requests.get("https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69?api-key=579b464db66ec23bdd000001fac7277b9e444f4f5c1abfd7d2dc9105&format=json&offset=" + str(offset) +"&limit=" + str(limit)).json()
		if 'error' not in JSONContent1:
			offset = offset + limit
			JSONContent['records']=[*JSONContent['records'] , *JSONContent1['records']]


	pol_recs=pd.DataFrame.from_records(JSONContent['records'],index='id')
#    pol_recs['displayname'] = pol_recs.apply(lambda row: display_name(row), axis=1)

	json_updated=JSONContent['updated']
	last_update=pd.to_datetime(pol_recs.last_update.unique())[0]
	stations=len(pol_recs.station.unique())
	stations_df=pd.read_csv("air_pol_stations.csv",encoding='cp1252')
	df= [pol_recs, stations_df, total, last_update, stations, json_updated]
	#stations_df
	return df

@st.cache
def get_location(station):
	r=( (stations_df[stations_df['Station']==station][['latitude']].values[0][0]), (stations_df[stations_df['Station']==station][['longitude']].values[0][0]))
	return r



def get_popup(station):
	return pol_recs[pol_recs['station']==station][['pollutant_id','pollutant_min', 'pollutant_avg','pollutant_max']].reset_index(drop=True).set_index('pollutant_id')



def mapbuilder(pol_recs):
	# center to the mean of all points
	m = folium.Map(location=(21,81), zoom_start=4.5)
	#m
	#marker_cluster = MarkerCluster().add_to(m)

	for i in pol_recs.station.unique():
		location = get_location(i.rstrip())
		#print(location)
		html = get_popup(i).to_html(classes='table table-striped table-hover table-condensed table-responsive',table_id=str(i))
		#print(html)
		folium.Marker(location=location,
							popup = folium.Popup(html),
							tooltip=str(i))\
		.add_to(m)

	# display the map

	m.save('map.html')
	return m


df=JSON_Downloader()
pol_recs=df[0]
stations_df=df[1]
#my_bar.progress(1.0)
noofstations=df[4]
#last_update=datetime.strptime(df[3], '%d-%m-%Y %H:%M:%S' )
last_refreshed=datetime.now()
#.strftime("%d %B %Y, %H:%M:%S")
dataset_updated=datetime.fromtimestamp(int(df[5]))
#.strftime("%d %B %Y, %H:%M:%S")
map=mapbuilder(pol_recs)
update_data=pd.DataFrame([datetime.now(),datetime.fromtimestamp(int(df[5])),df[3]])
update_data.to_hdf('store.h5',key='update_data',mode='w')
