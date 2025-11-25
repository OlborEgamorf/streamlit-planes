import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from functions import *

def scatterplot(dataX, dataY, pays, colonneX, titre=None):
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

    if pays is None:
        return
    

    dataX = (
        dataX.groupby(["COUNTRY_NAME"])[colonneX]
        .sum()
        .reset_index(name="VALUE_X")
    )

    print(dataX)

    dataY = (
        dataY.groupby(["COUNTRY_NAME"])["CO2_EMISSIONS_TONNES"]
        .sum()
        .reset_index(name="VALUE_Y")
    )

    df = pd.merge(dataX, dataY, on=["COUNTRY_NAME"])
    print(df)

    fig = go.Figure()

    # Courbe du pays
    fig.add_trace(
        go.Scatter(
            x=df["VALUE_X"],
            y=df["VALUE_Y"],
            text=df["COUNTRY_NAME"],
            mode="markers",
            marker=dict(
                size=[12 if el == pays else 8 for el in df["COUNTRY_NAME"]],
                opacity=[1 if el == pays else 0.2 for el in df["COUNTRY_NAME"]],
                color=["gold" if el == pays else "cyan" for el in df["COUNTRY_NAME"]],
                line=dict(width=0)
            )
        )
    )


    # --- Mise en forme ---
    fig.update_layout(
        title=titre or f"Évolution des émissions de CO2 VS passagers en vol",
        xaxis_title="Nombre de passagers",
        yaxis_title="Emissions de CO2",
        template="plotly_white",
        legend_title="Légende",
    )

    # Affichage dans Streamlit
    st.plotly_chart(fig)