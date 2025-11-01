import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium


def displayMap():

    
    
    m = folium.Map([48.59942120882304, 15.710549454957945], tiles="cartodbpositron", zoom_start=4)
    folium.GeoJson("data/europe.geojson",
                   style_function=lambda feature: {
                        "fillColor": "#ffff0000",
                        "color": "black",
                        "weight": 0.5,
                    },
    ).add_to(m)
    # m.fit_bounds([[36.61683092620905, -10.367651872713363], [71.15207057472252, 46.33659126976786]])

    st_data = st_folium(m)