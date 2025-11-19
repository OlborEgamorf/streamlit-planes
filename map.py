import streamlit as st
import geopandas as gpd
import plotly.express as px

def displayMap(data, col, country):

    

    # data["FIPS"] = data["COUNTRY_ID"]

    data = data[data["YEAR"] == 2022]

    fig = px.choropleth(data, geojson=gpd.read_file("data/europe.geojson"), locations='COUNTRY_ID', color=col,
                            color_continuous_scale="Viridis",
                            scope="europe",
                            labels={col:'AH'},
                            featureidkey='properties.ISO2'
                            )
    fig.update_layout({"margin":{"r":0,"t":0,"l":0,"b":0}, "plot_bgcolor":"rgba(0, 0, 0, 0)", "paper_bgcolor":"rgba(0, 0, 0, 0)"})
    fig.update_geos(fitbounds="locations", visible=False) 

    event = st.plotly_chart(fig, on_select="rerun", selection_mode=["points"])

    # st.write(event)
    points = event["selection"].get("points", [])

    if points:
        first_point = points[0]
        country = first_point["properties"].get("NAME", None)
    else:
        country = "Italy"
    
    return country