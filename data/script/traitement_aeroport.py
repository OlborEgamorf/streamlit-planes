import pandas as pd

file = "data/raw/vols_par_aeroport.csv"
df = pd.read_csv(file, delimiter=",")

# df_arr = df[df["Traffic and transport measurement"] == "Passengers on board (arrivals)"]
# df_dep = df[df["Traffic and transport measurement"] == "Passengers on board (departures)"]

df_arr = df[df["Traffic and transport measurement"] == "Commercial passenger air flights (arrivals)"]
df_dep = df[df["Traffic and transport measurement"] == "Commercial passenger air flights (departures)"]

# Retrait des colonnes inutiles
df_arr = df_arr.drop(columns=["STRUCTURE", "STRUCTURE_ID", "STRUCTURE_NAME", "freq", "Time frequency", "unit", "Unit of measure", "tra_meas", "Traffic and transport measurement", "schedule", "Type of schedule", "tra_cov", "Transport coverage", "CONF_STATUS", "Confidentiality status (flag)", "Time", "Observation status (Flag) V2 structure", "Observation value", "OBS_FLAG"])
df_dep = df_dep.drop(columns=["STRUCTURE", "STRUCTURE_ID", "STRUCTURE_NAME", "freq", "Time frequency", "unit", "Unit of measure", "tra_meas", "Traffic and transport measurement", "schedule", "Type of schedule", "tra_cov", "Transport coverage", "CONF_STATUS", "Confidentiality status (flag)", "Time", "Observation status (Flag) V2 structure", "Observation value", "OBS_FLAG"])

# Ajout d'un ID par pays
df_arr["COUNTRY_ID"] = df_arr["rep_airp"].apply(lambda x: x.split("_")[0])
df_dep["COUNTRY_ID"] = df_dep["rep_airp"].apply(lambda x: x.split("_")[0])

# Rename des colonnes
df_arr = df_arr.rename(columns={"rep_airp":"AIRPORT_ID", "Reporting airport":"AIRPORT_NAME", "TIME_PERIOD":"TIME", "OBS_VALUE":"ARRIVAL_VALUE"})
df_dep = df_dep.rename(columns={"rep_airp":"AIRPORT_ID", "Reporting airport":"AIRPORT_NAME", "TIME_PERIOD":"TIME", "OBS_VALUE":"DEPARTURE_VALUE"})

# Reorder des colonnes
cols = df_arr.columns.tolist()
cols = cols[-1:] + cols[:-1]
df_arr = df_arr[cols]

cols = df_dep.columns.tolist()
cols = cols[-1:] + cols[:-1]
df_dep = df_dep[cols]

df = pd.merge(df_arr, df_dep, on=["AIRPORT_ID", "AIRPORT_NAME", "TIME", "COUNTRY_ID"])

# Sauvegarde
df.to_csv("vols_par_aeroport_traite.csv", index=False)