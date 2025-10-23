import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

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

    # --- Création du graphique avec graph_objects pour plus de contrôle ---
    fig = go.Figure()

    # Courbe du pays
    fig.add_trace(
        go.Scatter(
            x=df[colonne_x],
            y=df[colonne_y1],
            mode="lines",
            name=f"{colonne_y1} ({pays})",
            line=dict(color="lightblue", width=2)
        )
    )

    # Ligne de moyenne globale
    fig.add_trace(
        go.Scatter(
            x=[df[colonne_x].min(), df[colonne_x].max()],
            y=[moyenne_globale, moyenne_globale],
            mode="lines",
            name="Moyenne globale",
            line=dict(color="red", dash="dash")
        )
    )

    # --- Mise en forme ---
    fig.update_layout(
        title=titre or f"Évolution de {colonne_y1} pour {pays}",
        xaxis_title="Années",
        yaxis_title="Valeur",
        template="plotly_white",
        legend_title="Légende",
    )

    # Affichage dans Streamlit
    st.plotly_chart(fig, use_container_width=True)
