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
data_passagers_pays = pd.read_csv("data/passagers_par_pays_traite2.csv")
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
st.markdown("<h1 style='text-align: center; margin:0px;'>Streamlit Planes : Analyse des Données de l'Aviation Européenne</h1>", unsafe_allow_html=True)

# Générer automatiquement une liste d'années
years = list(range(2000, 2025))  
years_co2 = list(range(2000, 2025))  

# Barre d'onglets
tab0, tab1, tab2, tab3 = st.tabs(["Accueil","Analyse globale", "Analyse exploratoire", "Impact Environnemental"])

with tab0:
    # Problématique
    st.markdown("### Problématique Analysée")
    st.markdown("""
    L'aviation est un secteur clé de l'économie, mais également un contributeur significatif aux émissions de $\\text{CO}_2$. 
    Notre analyse vise à répondre à la question suivante :
    
    > **Comment les **flux aériens** (vols et passagers) et les **émissions de $\\text{CO}_2$** de l'aviation ont-ils **évolué dans les pays européens** au cours des deux dernières décennies (**2000-2024**), et quels **aéroports** ont été les moteurs de ces changements ?**
    
    L'objectif est d'offrir une **vue détaillée et interactive** de la dynamique du transport aérien en Europe pour mieux comprendre ses tendances et ses impacts.
    """)
    st.markdown("---")

    # Fonctionnalités
    st.markdown("### Fonctionnalités et Capacités d'Analyse")
    st.markdown("""
    Cette application interactive, développée avec **Streamlit**, vous permet d'explorer les données de l'aviation européenne via deux onglets principaux :
    
    * **Accueil (ceci) :** Présentation du projet et de la problématique.
    * **Analyse globale :** Offre un aperçu macroscopique, comparant un pays sélectionné (par défaut la France) à la moyenne européenne.
        * **Carte interactive** pour la sélection de pays.
        * **Évolution des vols** (Arrivées/Départs) dans le temps (Line Chart).
        * **Top 5 des aéroports** les plus fréquentés par pays (Bar Chart).
        * **Évolution des émissions de $\\text{CO}_2$** liées à l'aviation (Line Chart).
    * **Analyse exploratoire :** Permet une plongée détaillée au niveau d'un aéroport spécifique.
        * **Graphique en double barre** montrant l'évolution des **passagers** (Arrivées/Départs) pour un aéroport sélectionné.
        * **Graphique en double ligne** montrant l'évolution des **vols** (Arrivées/Départs) pour un aéroport sélectionné.
        
    **Interactivité :** Utilisez les **sliders d'années** et les **selectboxes** (Pays, Aéroports, Arrivées/Départs) pour personnaliser votre exploration.
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

        column_name_line = "ARRIVAL_VALUE" if type_data == "Arrivées" else "DEPARTURE_VALUE"
        
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

        country_name = map.displayMap(filtered_data_vols_pays, column_name_line, country_name)
        # On affiche le graphique pour la France VS l'Europe
        line_chart(filtered_data_vols_pays, country_name, "TIME", column_name_line, f"Évolution des vols pour {country_name}")


    
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
        
        
### ---------------- TAB 3 IMPACT ENVIRONNEMENTAL -------------------------------------------------------
with tab3:
    
    
    st.markdown("### Analyse de l'Impact Environnemental de l'Aviation en Europe")
    st.markdown("""
    Dans cette section, nous explorons en détail les émissions de $\\text{CO}_2$ liées à l'aviation dans les pays européens. 
    Utilisez le slider ci-dessous pour sélectionner une plage d'années spécifique et observer comment les émissions ont évolué au fil du temps.
    """)
    
    # 1. Définition des colonnes (ex: ratio 10:1:10 pour le contenu et le séparateur)
    col1, separator, col2 = st.columns([10, 1, 10]) 


    # 2. Injection du CSS pour le séparateur
    with separator:
        st.markdown(
            """
            <style>
            .vertical-line {
                border-left: 0.5px solid #E6DFDF; 
                min-height: 100vh;
                margin-left: 50%;             
            }
            </style>
            <div class='vertical-line'></div>
            """, 
            unsafe_allow_html=True
        )

    with col1: 
        col3, col4 = st.columns([2, 1])
        
        with col4:
            
            N_countries = st.number_input(
                "Sélectionnez le nombre de pays à afficher :",
                min_value=1,
                max_value=len(data_co2_pays["COUNTRY_NAME"].unique()), # Max le nombre total de pays
                value=5, # Valeur par défaut
                step=1
            )
        with col3:
        
            # Slider pour sélectionner la plage d'années
            start_year_env, end_year_env = st.slider(
                "Sélectionne une plage d'années pour l'analyse environnementale",
                min_value=years_co2[0],
                max_value=years_co2[-1],
                value=(2020, 2024),
                key="slider_tab3"
            )
        
       
        # Filtrage des données en fonction de la plage d'années sélectionnée
        filtered_data_co2_env = data_co2_pays[
            (data_co2_pays["YEAR"] >= start_year_env) & (data_co2_pays["YEAR"] <= end_year_env)
        ]
        
        data_passagers_pays["YEAR"] = data_passagers_pays["TIME"].str[:4].astype(int)
        data_passagers_pays = data_passagers_pays.sort_values("TIME")

        filtered_data_passagers_env = data_passagers_pays[
            (data_passagers_pays["YEAR"] >= start_year_env) & (data_passagers_pays["YEAR"] <= end_year_env)
        ]   
        
   
        st.markdown(f"## Évolution des émissions de CO₂ des {N_countries} Pays les plus polluants")
    
    
        top_countries = top_N(filtered_data_co2_env, "YEAR", "CO2_EMISSIONS_TONNES", N_countries)
        
        top_n_line_chart(
            filtered_data_co2_env,
            colonne_x="YEAR",
            colonne_y="CO2_EMISSIONS_TONNES",
            top_n=N_countries
        )
    

    with col2:
        col5, col6 = st.columns([1, 1])
        with col5:
            departures = st.selectbox(
                        "Sélectionne Arrivées ou Départs",
                        options=["Arrivées", "Départs"],
                        index=0,
                        key="selectbox_tab3"
            )
            column_name_env = "ARRIVAL_VALUE" if departures == "Arrivées" else "DEPARTURE_VALUE"
           
        
        st.markdown(f"## Évolution des Passagers ({departures}) pour ces pays")

        top_n_passagers_barchart_aggregated(
            filtered_data_passagers_env,
            top_countries,
            departure_col=column_name_env,
            titre=f"Évolution des Passagers ({departures}) des {N_countries} Pays les plus polluants"
        )