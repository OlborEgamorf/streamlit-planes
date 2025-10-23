import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from linechart import *

# Import des données
data_vols_pays = pd.read_csv("data/vols_par_pays_traite.csv")

# Settings
width_px = 2000
st.set_page_config(page_title="Streamlit Planes", layout="wide", initial_sidebar_state="expanded")
st.markdown(f"<style>.reportview-container .main .block-container{{max-width: {width_px}px;}}</style>", unsafe_allow_html=True)

# Titre centré en haut
st.markdown("<h1 style='text-align: center; margin-top:10px;'>Streamlit Planes - Flight Data Analysis</h1>", unsafe_allow_html=True)

# Générer automatiquement une liste d'années
years = list(range(2015, 2026))  

# Barre d'onglets
tab1, tab2 = st.tabs(["Analyse globale", "Analyse exploratoire"])




with tab1:
    # Création des deux colonnes
    col1, col2 = st.columns([1, 1]) 
    
    with col2:  
        #Slider des années
        start_year, end_year = st.slider(
            "Sélectionne une plage d'années",
            min_value=years[0],
            max_value=years[-1],
            value=(2020, 2024)
        )      
        
        st.write(f"Plage sélectionnée : {start_year} → {end_year}")
        

    # --- PARTIE GAUCHE : CARTE ---
    with col1:
        data = pd.DataFrame({
            'lat': [48.8566, 52.5200, 41.9028, 40.4168],  # Paris, Berlin, Rome, Madrid
            'lon': [2.3522, 13.4050, 12.4964, -3.7038]
        })
        st.map(data, zoom=2.5)
    
        # Graphique Line chart Pays VS Moyenne Globale
        
        # Conversion de la colonne TIME en entier
        data_vols_pays["YEAR"] = data_vols_pays["TIME"].str[:4].astype(int)
        data_vols_pays = data_vols_pays.sort_values("TIME")

        # Puis ton filtrage
        filtered_data = data_vols_pays[
            (data_vols_pays["YEAR"] >= start_year) & (data_vols_pays["YEAR"] <= end_year)
        ]

        # On affiche le graphique pour la France VS l'Europe
        pays = "France"
        line_chart(filtered_data, pays, "TIME", "VALUE", f"Évolution des vols pour {pays}")

    # --- PARTIE DROITE : SLIDER + GRAPHIQUE ---
    
        