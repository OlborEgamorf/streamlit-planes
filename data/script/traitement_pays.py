import pandas as pd

file = "data/raw/vols_par_pays.csv"
df = pd.read_csv(file, delimiter=",")

# Retrait des colonnes inutiles
df = df.drop(columns=["STRUCTURE", "STRUCTURE_ID", "STRUCTURE_NAME", "freq", "Time frequency", "unit", "Unit of measure", "tra_meas", "Traffic and transport measurement", "schedule", "Type of schedule", "tra_cov", "Transport coverage", "CONF_STATUS", "Confidentiality status (flag)", "Time"])

# Rename des colonnes
df = df.rename(columns={"Geopolitical entity (reporting)":"COUNTRY_NAME", "TIME_PERIOD":"TIME", "OBS_VALUE":"VALUE", "Observation value":"OBS_VALUE", "Observation status (Flag) V2 structure":"OBS_V2", "geo":"COUNTRY_ID"})

# Sauvegarde
df.to_csv("vols_par_pays_traite.csv", index=False)