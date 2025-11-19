from functions import *
import plotly.express as px
import streamlit as st

def barchart_top_aeroport(data, countryID, departure, top_n=5, titre=None):
    """
    Affiche un graphique en barres des top N aéroports les plus fréquentés pour un pays donné.

    Parameters
    ----------
    data : pd.DataFrame
        Le DataFrame contenant les données des vols.
    countryID : str
        Le code du pays à filtrer (ex: 'FR').
    departure : str
        Le type de vol à filtrer (ex: 'Arrivées' ou 'Départs').
    top_n : int
        Le nombre d'aéroports à afficher.
    titre : str (optionnel)
        Le titre du graphique.
    """

    print(countryID)
    if countryID is None:
        st.write("CHOISIR")
    
    else:
        # Obtenir les top N aéroports
        top_airports_df = top_airports_by_country(data, countryID, top_n, departure)

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
        st.plotly_chart(fig, width="stretch")


def double_barChart(data, countryID, aeroport_name, titre=None):
    """ 
    Affiche par année le nombre d'arrivées et de départs pour un aéroport donné.
    
    Parameters
    ----------
    data: pd.DataFrame
        Le DataFrame contenant les données des vols.
    countryID : str
        Le code du pays à filtrer (ex: 'FR').
    aeroport_name : str
        Le nom de l'aéroport à analyser.
    titre : str (optionnel)
        Le titre du graphique.
    """

    # 1. Filtrer sur le pays et l'aéroport
    airport_data = data[(data["COUNTRY_ID"] == countryID) & 
                        (data["AIRPORT_NAME"] == aeroport_name)]

    if airport_data.empty:
        st.warning(f"Aucune donnée trouvée pour l'aéroport : **{aeroport_name}**")
        return

    # 2. Agrégation des données (Correction : utilisation de 'sum')
    grouped = airport_data.groupby("YEAR").agg(
        arrivals=("ARRIVAL_VALUE", 'sum'),
        departures=("DEPARTURE_VALUE", 'sum')
    ).reset_index()

    # 3. Mise en forme pour Plotly (format long)
    df_chart = grouped.melt(id_vars="YEAR", 
                            value_vars=["arrivals", "departures"],
                            var_name="Type de Vol",
                            value_name="Nombre de Vols")

    # 4. Renommer les valeurs pour un affichage propre
    df_chart["Type de Vol"] = df_chart["Type de Vol"].replace(
        {"arrivals": "Arrivées", "departures": "Départs"}
    )

    # 5. Créer le graphique avec les nouvelles couleurs
    fig = px.bar(
        df_chart,
        x="YEAR",
        y="Nombre de Vols",
        color="Type de Vol",
        barmode="group",
        title=titre or f"Évolution Arrivées / Départs (personnes) pour {aeroport_name}",
        labels={"YEAR": "Année", "Nombre de Vols": "Nombre total de vols"},
        # COULEURS MISES À JOUR
        color_discrete_map={"Arrivées": "lightblue", "Départs": "lightcoral"}
    )
    
    # 6. Mise à jour de l'affichage pour l'espacement
    fig.update_layout(
        # Espacement entre les groupes de barres (ici, les années)
        bargap=0.3,
        # Espacement entre les barres à l'intérieur d'un même groupe (Arrivées/Départs)
        bargroupgap=0.15 
    )
    
    # 7. Affichage
    st.plotly_chart(fig, width="stretch")