import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


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
    col1, col2 = st.columns([2, 1])  # Proportions égales

    # --- PARTIE GAUCHE : CARTE ---
    with col1:
        data = pd.DataFrame({
            'lat': [48.8566, 52.5200, 41.9028, 40.4168],  # Paris, Berlin, Rome, Madrid
            'lon': [2.3522, 13.4050, 12.4964, -3.7038]
        })
        st.map(data, zoom=2.5)

    # --- PARTIE DROITE : SLIDER + GRAPHIQUE ---
    with col2:        
        # Slider au-dessus du graphique
        start_year, end_year = st.slider(
            "Sélectionne une plage d'années",
            min_value=years[0],
            max_value=years[-1],
            value=(2020, 2024)
        )

        st.write(f"Plage sélectionnée : {start_year} → {end_year}")
        
        # Graphique
        chart_data = pd.DataFrame(np.random.randn(20, 2), columns=["A", "B"])
        st.line_chart(chart_data)
