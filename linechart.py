import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from functions import *

def line_chart(data, pays, colonne_x, departure, titre=None):
    """
    Crée un graphique linéaire pour un pays donné avec une ligne horizontale
    représentant la moyenne globale.

    Paramètres :
    ------------
    data : pd.DataFrame
        Jeu de données contenant les colonnes nécessaires
    pays : str
        Nom du pays à filtrer
    colonne_x : str
        Nom de la colonne pour l'axe des x
    departure : str
        Nom de la colonne pour l'axe des y
    titre : str (optionnel)
        Titre du graphique
    """

    # Filtrage du pays
    df = data[data["COUNTRY_NAME"] == pays]

    # Calcul de la moyenne globale
    moyenne_par_annee = data.groupby(colonne_x)[departure].mean().reset_index()

    fig = go.Figure()

    # Courbe du pays
    fig.add_trace(
        go.Scatter(
            x=df[colonne_x],
            y=df[departure],
            mode="lines",
            name=f"{departure} ({pays})",
            line=dict(color="lightblue", width=2)
        )
    )

    # Ligne de moyenne globale
    fig.add_trace(
        go.Scatter(
            x=moyenne_par_annee[colonne_x],
            y=moyenne_par_annee[departure],
            mode="lines",
            name="Moyenne globale par année",
            line=dict(color="red", dash="dash")
        )
    )


    # --- Mise en forme ---
    fig.update_layout(
        title=titre or f"Évolution de {departure} pour {pays}",
        xaxis_title="Années",
        yaxis_title="Valeur",
        template="plotly_white",
        legend_title="Légende",
    )

    # Affichage dans Streamlit
    st.plotly_chart(fig, width="stretch")


def double_line_chart(data, idpays, aeroport, colonne_x, titre=None):
    """
    Crée un graphique linéaire avec deux courbes pour un pays donné.
    Paramètres :
    ------------
    data : pd.DataFrame
        Jeu de données contenant les colonnes nécessaires
    idpays : int
        ID du pays à filtrer
    aeroport : str
        Nom de l'aéroport à filtrer
    colonne_x : str
        Nom de la colonne pour l'axe des x
    titre : str (optionnel)
        Titre du graphique
    """

    data_pays = data[data["COUNTRY_ID"] == idpays]
    fig = go.Figure()
    # Courbe des arrivées
    fig.add_trace(
        go.Scatter(
            x=data_pays[data_pays["AIRPORT_NAME"] == aeroport][colonne_x],
            y=data_pays[data_pays["AIRPORT_NAME"] == aeroport]["ARRIVAL_VALUE"],
            mode="lines",
            name="Arrivées",
            line=dict(color="lightblue", width=2)
        )
    )
    
    # Courbe des départs
    fig.add_trace(
        go.Scatter(
            x=data_pays[data_pays["AIRPORT_NAME"] == aeroport][colonne_x],
            y=data_pays[data_pays["AIRPORT_NAME"] == aeroport]["DEPARTURE_VALUE"],
            mode="lines",
            name="Départs",
            line=dict(color="lightcoral", width=2)
        )
    )
    # --- Mise en forme ---
    fig.update_layout(
        title=titre or f"Évolution des Arrivées et Départs pour le pays ID {idpays}",
        xaxis_title="Années",
        yaxis_title="Valeur",
        template="plotly_white",
        legend_title="Légende",
    )

    # Affichage dans Streamlit
    st.plotly_chart(fig, width="stretch")