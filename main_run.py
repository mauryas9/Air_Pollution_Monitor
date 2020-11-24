import streamlit as st
import pandas as pd
#import json
import time
from datetime import datetime
#import folium
#from folium.plugins import MarkerCluster
#from streamlit_folium import folium_static
import streamlit.components.v1 as components

st.title('Real Time Monitoring of Air Pollution')
st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#e04938,#e86354);
    color: white;
}
</style>
""",
	unsafe_allow_html=True,
)
st.sidebar.header("Coded by Maurya S.")
st.sidebar.write("Datasource: www.data.gov.in, refreshed hourly with one hour delay")
update_data=pd.read_hdf('store.h5', 'update_data')
print(update_data)
@st.cache
def mapfile(update_data):
	HtmlFile = open("map.html", 'r', encoding='utf-8')
	source_code = HtmlFile.read()
	HtmlFile.close()
	return source_code
st.write("Showing data for " + update_data[0][2].strftime("%d %B %Y, %H:%M:%S"))
components.html(mapfile(update_data[0][0]),height=600)

#dataset_updated=update_data[0][1]
#@st.cache(suppress_st_warning=True,ttl=1800)
def dataupdate():
	import data_updater
	#datetime.now().strftime("%d %B %Y, %H:%M:%S")
	pass

if (datetime.now()-update_data[0][1]).seconds>1000 :
	dataupdate()
st.write("Dataset last updated at " + update_data[0][0].strftime("%d %B %Y, %H:%M:%S"))