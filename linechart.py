import plotly.express as px
import streamlit as st

def line_chart(data, pays, colonne_x, colonne_y1, titre=None):
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
    colonne_y1 : str
        Nom de la variable à représenter
    titre : str (optionnel)
        Titre du graphique
    """

    # Filtrage du pays
    df = data[data["COUNTRY_NAME"] == pays]

    # Calcul de la moyenne globale
    moyenne_globale = data[colonne_y1].mean()

    # Création du graphique principal
    fig = px.line(
        df,
        x=colonne_x,
        y=colonne_y1,
        title=titre or f"Évolution de {colonne_y1} pour {pays}",
        labels={colonne_x: "Années", colonne_y1: "Valeur"}
    )

    # Ajout de la ligne de moyenne globale
    fig.add_hline(
        y=moyenne_globale,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Moyenne globale ({moyenne_globale:.2f})",
        annotation_position="bottom right"
    )

    # Personnalisation du graphique
    fig.update_layout(
        template="plotly_white",
        legend_title="",
    )

    st.plotly_chart(fig, use_container_width=True)
