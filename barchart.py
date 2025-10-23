from functions import *
import plotly.express as px
import streamlit as st

def barchart_top_aeroport(data, countryID, top_n=5, titre=None):
    """
    Affiche un graphique en barres des top N aéroports les plus fréquentés pour un pays donné.

    Parameters
    ----------
    data : pd.DataFrame
        Le DataFrame contenant les données des vols.
    countryID : str
        Le code du pays à filtrer (ex: 'FR').
    top_n : int
        Le nombre d'aéroports à afficher.
    titre : str (optionnel)
        Le titre du graphique.
    """

    # Obtenir les top N aéroports
    top_airports_df = top_airports_by_country(data, countryID, top_n)

    # Créer le graphique en barres
    fig = px.bar(
        top_airports_df,
        x="AIRPORT_NAME",
        y="TOTAL_FLIGHTS",
        title=titre or f"Top {top_n} Aéroports les plus fréquentés pour {countryID}",
        labels={"AIRPORT_NAME": "Aéroport", "TOTAL_FLIGHTS": "Nombre total de vols"},
        color_discrete_sequence=["steelblue"] 
    )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig, use_container_width=True)


def double_barChart(data, countryID, aeroport_name, titre=None):
    """ 
    Affiche un graphique en barres comparant le nombre d'arrivées et de départs pour un aéroport donné.
    Parameters
    ----------
    data : pd.DataFrame
        Le DataFrame contenant les données des vols.
    countryID : str
        Le code du pays à filtrer (ex: 'FR').
    aeroport_name : str
        Le nom de l'aéroport à analyser.
    titre : str (optionnel)
        Le titre du graphique.

    """
    