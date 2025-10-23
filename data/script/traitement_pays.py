import pandas as pd

file = "data/raw/passagers_par_pays.csv"
df = pd.read_csv(file, delimiter=",")

# df_arr = df[df["Traffic and transport measurement"] == "Passengers on board (arrivals)"]
# df_dep = df[df["Traffic and transport measurement"] == "Passengers on board (departures)"]

df_arr = df[df["Traffic and transport measurement"] == "Commercial passenger air flights (arrivals)"]
df_dep = df[df["Traffic and transport measurement"] == "Commercial passenger air flights (departures)"]

# Retrait des colonnes inutiles
df_arr = df_arr.drop(columns=["STRUCTURE", "STRUCTURE_ID", "STRUCTURE_NAME", "freq", "Time frequency", "unit", "Unit of measure", "tra_meas", "Traffic and transport measurement", "schedule", "Type of schedule", "tra_cov", "Transport coverage", "CONF_STATUS", "Confidentiality status (flag)", "Time", "Observation value", "Observation status (Flag) V2 structure", "OBS_FLAG"])
df_dep = df_dep.drop(columns=["STRUCTURE", "STRUCTURE_ID", "STRUCTURE_NAME", "freq", "Time frequency", "unit", "Unit of measure", "tra_meas", "Traffic and transport measurement", "schedule", "Type of schedule", "tra_cov", "Transport coverage", "CONF_STATUS", "Confidentiality status (flag)", "Time", "Observation value", "Observation status (Flag) V2 structure", "OBS_FLAG"])

# Rename des colonnes
df_arr = df_arr.rename(columns={"Geopolitical entity (reporting)":"COUNTRY_NAME", "TIME_PERIOD":"TIME", "OBS_VALUE":"ARRIVAL_VALUE", "geo":"COUNTRY_ID"})
df_dep = df_dep.rename(columns={"Geopolitical entity (reporting)":"COUNTRY_NAME", "TIME_PERIOD":"TIME", "OBS_VALUE":"DEPARTURE_VALUE", "geo":"COUNTRY_ID"})

df = pd.merge(df_arr, df_dep, on=["COUNTRY_ID","COUNTRY_NAME","TIME"])

# Sauvegarde
df.to_csv("data/passagers_par_pays_traite.csv", index=False)