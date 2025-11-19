import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import map
from linechart import *
from functions import *
from barchart import *


st.markdown("<style> .st-emotion-cache-zy6yx3 {padding-top: 0rem; padding-bottom: 0rem;} </style>", unsafe_allow_html=True)


# Import des données
data_vols_pays = pd.read_csv("data/vols_par_pays_traite.csv")
data_vols_aeroport = pd.read_csv("data/vols_par_aeroport_traite.csv")
data_passagers_aeroport = pd.read_csv("data/passagers_par_aeroport_traite.csv")
data_passagers_pays = pd.read_csv("data/passagers_par_pays_traite.csv")
data_co2_pays = pd.read_csv("data/co2_par_pays.csv")

# paramètres généraux
country_name = "France"
countryIDPays = get_ID_Pays(data_vols_pays, country_name)


# -------------------------------------------------------
# Settings
width_px = 2000
st.set_page_config(page_title="Streamlit Planes", layout="wide", initial_sidebar_state="expanded")
st.markdown(f"<style >.reportview-container .main .block-container{{max-width: {width_px}px; margin:0px;}}</style>", unsafe_allow_html=True)

# Titre centré en haut
st.markdown("<h1 style='text-align: center; margin:0px;'>Streamlit Planes - Flight Data Analysis</h1>", unsafe_allow_html=True)

# Générer automatiquement une liste d'années
years = list(range(2000, 2025))  

# Barre d'onglets
tab0, tab1, tab2 = st.tabs(["Accueil","Analyse globale", "Analyse exploratoire"])

with tab0:
    st.markdown("## Bienvenue dans l'application Streamlit Planes")
    st.markdown("""
    Cette application permet d'analyser les données de vols internationaux, y compris les arrivées, départs, passagers et émissions de CO₂.
    
    ### Instructions :
    - Utilisez l'onglet **Analyse globale** pour visualiser les tendances des vols et des émissions de CO₂ pour un pays spécifique.
    - Utilisez l'onglet **Analyse exploratoire** pour explorer les données par aéroport et comparer les arrivées et départs.
    
    ### Sources de données :
    - Données de vols internationaux
    - Données d'émissions de CO₂ liées à l'aviation
    
    Amusez-vous bien en explorant les données !
    """)

with tab1:
    # Création des deux colonnes
    col1, col2 = st.columns([1, 1]) 

    with col2:
        departure, slider = st.columns([1, 2])
        with departure:
            type_data = st.selectbox(
                    "Sélectionne Arrivées ou Départs",
                    options=["Arrivées", "Départs"],
                    index=0
            )
        
        with slider:
            #Slider des années
            start_year, end_year = st.slider(
                "Sélectionne une plage d'années",
                min_value=years[0],
                max_value=years[-1],
                value=(2020, 2024),
                key="slider_tab1"
            )
    
    ##### Graphique Line chart Pays VS Moyenne Globale
    # Conversion de la colonne TIME en entier
    data_vols_pays["YEAR"] = data_vols_pays["TIME"].str[:4].astype(int)
    data_vols_pays = data_vols_pays.sort_values("TIME")

    # Puis ton filtrage
    filtered_data_vols_pays = data_vols_pays[
        (data_vols_pays["YEAR"] >= start_year) & (data_vols_pays["YEAR"] <= end_year)
    ]

    with col1:

        country_name = map.displayMap(filtered_data_vols_pays, "ARRIVAL_VALUE", country_name)
        # On affiche le graphique pour la France VS l'Europe
        line_chart(filtered_data_vols_pays, country_name, "TIME", "ARRIVAL_VALUE", f"Évolution des vols pour {country_name}")


    
    # --- PARTIE DROITE : SLIDER + GRAPHIQUE ---
    with col2:     
                
        # Affichage du graphique en barres des top aéroports pour la France
        data_vols_aeroport["YEAR"] = data_vols_aeroport["TIME"].str[:4].astype(int)
        data_vols_aeroport = data_vols_aeroport.sort_values("TIME")

        # Puis ton filtrage
        filtered_data_vols_aeroport = data_vols_aeroport[
            (data_vols_aeroport["YEAR"] >= start_year) & (data_vols_aeroport["YEAR"] <= end_year)
        ]
        
        
        data_co2_pays = data_co2_pays.sort_values("YEAR")

        # Puis ton filtrage
        filtered_data_co2_pays = data_co2_pays[
            (data_co2_pays["YEAR"] >= start_year) & (data_co2_pays["YEAR"] <= end_year)
        ]
        
        

        barchart_top_aeroport(
            filtered_data_vols_aeroport,
            countryIDPays,
            type_data,
            top_n=5,
            titre=f"Top 5 Aéroports les plus fréquentés en {country_name}"
        )       
        
        #line_chart(data_passagers_pays,country_name,"TIME", "ARRIVAL_VALUE" if type_data == "Arrivées" else "DEPARTURE_VALUE",f"Évolution des vols pour {country_name} ({type_data})")
        
        line_chart(
            filtered_data_co2_pays,
            country_name,
            "YEAR",
            "CO2_EMISSIONS_TONNES",
            f"Évolution des émissions de CO₂ liées à l’aviation en {country_name}"
        )
            
    # --- PARTIE GAUCHE : CARTE ---
    with col1:
        data = pd.DataFrame({
            'lat': [48.8566, 52.5200, 41.9028, 40.4168],  # Paris, Berlin, Rome, Madrid
            'lon': [2.3522, 13.4050, 12.4964, -3.7038]
        })
        st.map(data, zoom=2.5)
    
        ##### Graphique Line chart Pays VS Moyenne Globale
        # Conversion de la colonne TIME en entier
        data_vols_pays["YEAR"] = data_vols_pays["TIME"].str[:4].astype(int)
        data_vols_pays = data_vols_pays.sort_values("TIME")

        # Puis ton filtrage
        filtered_data_vols_pays = data_vols_pays[
            (data_vols_pays["YEAR"] >= start_year) & (data_vols_pays["YEAR"] <= end_year)
        ]
        
        column_name_line = "ARRIVAL_VALUE" if type_data == "Arrivées" else "DEPARTURE_VALUE"


        # On affiche le graphique pour la France VS l'Europe
        line_chart(filtered_data_vols_pays, country_name, "TIME", column_name_line, f"Évolution des vols pour {country_name}")
                

### ---------------- TAB 2 ANALYSE EXPLORATOIRE -------------------------------------------------------    
with tab2:
    col1, col2 = st.columns([1, 1])
    
    with col2:
         # Crée deux colonnes pour les selectboxes
        col_country, col_airport = st.columns(2)

        with col_country:
            country_name_select = st.selectbox(
                "Sélectionne un pays",
                options=data_vols_pays["COUNTRY_NAME"].unique(),
                index=list(data_vols_pays["COUNTRY_NAME"].unique()).index("France")
            )
            countryIDselect = get_ID_Pays(data_vols_pays, country_name_select)

        with col_airport:
            aeroport_name_select = st.selectbox(
                "Sélectionne un aéroport",
                options=data_vols_aeroport[data_vols_aeroport["COUNTRY_ID"] == countryIDselect]["AIRPORT_NAME"].unique(),
                index=0
            )
        

    # --- PARTIE DROITE : SLIDER + GRAPHIQUE ---
    with col2:        
        # Slider au-dessus du graphique
        start_year_page2, end_year_page2 = st.slider(
            "Sélectionne une plage d'années",
            min_value=years[0],
            max_value=years[-1],
            value=(2020, 2024),
            key="slider_tab2"
        )
        
        
        # Affichage du graphique en barres des top aéroports pour la France
        data_passagers_aeroport["YEAR"] = data_passagers_aeroport["TIME"].str[:4].astype(int)
        data_passagers_aeroport = data_passagers_aeroport.sort_values("TIME")

        # Puis ton filtrage
        data_passagers_aeroport = data_passagers_aeroport[
            (data_passagers_aeroport["YEAR"] >= start_year_page2) & (data_passagers_aeroport["YEAR"] <= end_year_page2)
        ]
        
        double_barChart(
            data_passagers_aeroport,
            countryIDselect,
            aeroport_name_select
        )
    
    with col1:
        data = pd.DataFrame({
            'lat': [48.8566, 52.5200, 41.9028, 40.4168],  # Paris, Berlin, Rome, Madrid
            'lon': [2.3522, 13.4050, 12.4964, -3.7038]
        })
        st.map(data, zoom=2.5)
        
        # Affichage du graphique en barres des top aéroports pour la France
        data_vols_aeroport["YEAR"] = data_vols_aeroport["TIME"].str[:4].astype(int)
        data_vols_aeroport = data_vols_aeroport.sort_values("TIME")

        # Puis ton filtrage
        filter_data_vols_aeroport = data_vols_aeroport[
            (data_vols_aeroport["YEAR"] >= start_year_page2) & (data_vols_aeroport["YEAR"] <= end_year_page2)
        ]
        
        double_line_chart(filter_data_vols_aeroport, countryIDselect, aeroport=aeroport_name_select, colonne_x="TIME", titre=f"Évolution des Arrivées / Départs (avions) pour {aeroport_name_select}")