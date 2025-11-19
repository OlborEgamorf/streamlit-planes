import pandas as pd

def top_airports_by_country(data, countryID, top_n=5, departure ="Arrivées"):
    """
    Retourne les top N aéroports les plus fréquentés pour un pays donné.

    Parameters
    ----------
    data : pd.DataFrame
        Le DataFrame contenant les données des vols.
    countryID : str
        Le code du pays à filtrer (ex: 'FR').
    top_n : int
        Le nombre d'aéroports à retourner.
    departure : str
        Le type de vol à filtrer (ex: 'Arrivées' ou 'Départs').
    Returns
    -------
    pd.DataFrame
        Un DataFrame contenant les top N aéroports et leur nombre total de vols.
    """

    # Filtrer les données pour le pays spécifié
    country_data = data[data["COUNTRY_ID"] == countryID]

    # Calculer le total de vols par aéroport
    column_name = "ARRIVAL_VALUE" if departure == "Arrivées" else "DEPARTURE_VALUE"
    country_data[column_name] = pd.to_numeric(country_data[column_name], errors="coerce")
    
    
    airport_counts = (
        country_data.groupby("AIRPORT_NAME")[column_name]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
    )

    # Convertir en DataFrame pour affichage
    top_airports_df = airport_counts.reset_index()
    top_airports_df.columns = ["AIRPORT_NAME", "TOTAL_FLIGHTS"]

    return top_airports_df


def get_ID_Pays(data, country_name):
    """
    Retourne l'ID du pays donné son nom.

    Parameters
    ----------
    data : pd.DataFrame
        Le DataFrame contenant les données des vols.
    country_name : str
        Le nom du pays (ex: 'France').

    Returns
    -------
    str
        L'ID du pays correspondant.
    """

    country_row = data[data["COUNTRY_NAME"] == country_name]
    if not country_row.empty:
        return country_row.iloc[0]["COUNTRY_ID"]
    else:
        return None