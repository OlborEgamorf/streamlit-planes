import pandas as pd

file = "data/raw/passagers_par_aeroport.csv"
df = pd.read_csv(file, delimiter=",")

# Retrait des colonnes inutiles
df = df.drop(columns=["STRUCTURE", "STRUCTURE_ID", "STRUCTURE_NAME", "freq", "Time frequency", "unit", "Unit of measure", "tra_meas", "Traffic and transport measurement", "schedule", "Type of schedule", "tra_cov", "Transport coverage", "CONF_STATUS", "Confidentiality status (flag)", "Time"])

# Ajout d'un ID par pays
df["COUNTRY_ID"] = df["rep_airp"].apply(lambda x: x.split("_")[0])

# Rename des colonnes
df = df.rename(columns={"rep_airp":"AIRPORT_ID", "Reporting airport":"AIRPORT_NAME", "TIME_PERIOD":"TIME", "OBS_VALUE":"VALUE", "Observation value":"OBS_VALUE", "Observation status (Flag) V2 structure":"OBS_V2"})

# Reorder des colonnes
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]

# Sauvegarde
df.to_csv("passagers_par_aeroport_traite.csv", index=False)