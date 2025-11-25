import streamlit as st
import geopandas as gpd
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def displayMap(data, col):

    data = (
        data.groupby(["COUNTRY_ID"])[col]
        .sum()
        .reset_index(name=f"{col}_SUM")
    )

    fig = px.choropleth(data, 
                            geojson=gpd.read_file("data/europe.geojson"), 
                            locations='COUNTRY_ID', 
                            color=f"{col}_SUM",
                            color_continuous_scale="Blues",
                            labels={"ARRIVAL_VALUE_SUM":'Arrivées', "DEPARTURE_VALUE_SUM":"Départs"},
                            featureidkey='properties.ISO2',
                            
    )

    fig.update_layout({"margin":{"r":0,"t":0,"l":0,"b":0}, "autosize":False})
    fig.update_geos(fitbounds="locations", visible=False, projection_type="natural earth", bgcolor='rgba(0,0,0,0)') 

    event = st.plotly_chart(fig, on_select="rerun", selection_mode=["points"])

    points = event["selection"].get("points", [])

    if points:
        first_point = points[0]
        country = first_point["properties"].get("NAME", None)
        st.session_state['country'] = country
    else:
        st.session_state['country'] = None


def displayMapAeroport(data, airports:pd.DataFrame):

    data = data[data["YEAR"] == 2022]

    fig = px.choropleth(data, geojson=gpd.read_file("data/europe.geojson"), locations='COUNTRY_ID',
                            color_continuous_scale="Blues",
                            labels={"ARRIVAL_VALUE":'Arrivées', "DEPARTURE_VALUE":"Départs"},
                            featureidkey='properties.ISO2'
                            )
    fig.update_layout({"margin":{"r":0,"t":0,"l":0,"b":0}, "autosize":False})
    fig.update_geos(fitbounds="locations", visible=False, projection_type="natural earth", bgcolor='rgba(0,0,0,0)') 

    airportsLatLng = pd.read_csv("data/airports.csv", delimiter=";")
    d = airportsLatLng.to_dict("records")
    airportsCountry = list(filter(lambda x:x["Airport"] in airports, d))

    airportsCountry = sorted(airportsCountry, key=lambda x:x["Airport"])
    airportsNames = list(map(lambda x:x["Airport"], airportsCountry))

    fig.add_trace(
        go.Scattergeo(
            lon=list(map(lambda x:x["lng"], airportsCountry)),
            lat=list(map(lambda x:x["lat"], airportsCountry)),
            text=airportsNames,    # optionnel
            mode="markers",
            marker=dict(
                size=8,
                opacity=0.8
            ),
            name="Points",
        )
    )

    fig.update_traces(
        hoverinfo="skip",
        hovertemplate=None,  # impératif sinon Plotly recrée un hover
        selector=dict(type="choropleth")
    )
    fig.update_traces(selector=dict(type='scattergeo'), mode='markers')

    event = st.plotly_chart(fig, on_select="rerun", selection_mode=["points"], key="map_aero")
    
    # st.write(event)
    points = event["selection"].get("points", [])

    if points:
        first_point = points[0]
        airport = first_point.get("text", None)
        airport = airportsNames.index(airport)
    else:
        airport = None
    
    return airport