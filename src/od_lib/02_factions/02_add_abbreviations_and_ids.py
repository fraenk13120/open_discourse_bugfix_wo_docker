from od_lib.definitions import path_definitions
import pandas as pd
import numpy as np


# input directory
FACTIONS_STAGE_01 = path_definitions.FACTIONS_STAGE_01

# output directory
DATA_FINAL = path_definitions.DATA_FINAL
DATA_FINAL.mkdir(parents=True, exist_ok=True)

factions = pd.read_pickle(FACTIONS_STAGE_01 / "factions.pkl")

abbreviations_dict = {
    "Alternative für Deutschland": "AfD",
    "Deutsche Soziale Union": "DSU",
    "Fraktion Alternative für Deutschland": "AfD",
    "Fraktion Bayernpartei": "BP",
    "Fraktion Bündnis 90/Die Grünen": "Bündnis 90/Die Grünen",
    "Fraktion DIE LINKE.": "DIE LINKE.",
    "Fraktion DP/DPB (Gast)": "DP/DPB",
    "Fraktion DRP (Gast)": "DRP",
    "Fraktion Demokratische Arbeitsgemeinschaft": "DA",
    "Fraktion Deutsche Partei": "DP",
    "Fraktion Deutsche Partei Bayern": "DPB",
    "Fraktion Deutsche Partei/Deutsche Partei Bayern": "DP/DPB",
    "Fraktion Deutsche Partei/Freie Volkspartei": "DP/FVP",
    "Fraktion Deutsche Reichspartei": "DRP",
    "Fraktion Deutsche Reichspartei/Nationale Rechte": "DRP/NR",
    "Fraktion Deutsche Zentrums-Partei": "Z",
    "Fraktion Deutscher Gemeinschaftsblock der Heimatvertriebenen und Entrechteten": "BHE",
    "Fraktion Die Grünen": "Bündnis 90/Die Grünen",
    "Fraktion Die Grünen/Bündnis 90": "Bündnis 90/Die Grünen",
    "Fraktion BÜNDNIS 90/DIE GRÜNEN": "Bündnis 90/Die Grünen",
    "Fraktion Freie Volkspartei": "FVP",
    "Fraktion Föderalistische Union": "FU",
    "Fraktion Gesamtdeutscher Block / Block der Heimatvertriebenen und Entrechteten": "GB/BHE",
    "Fraktion WAV (Gast)": "WAV",
    "Fraktion Wirtschaftliche Aufbauvereinigung": "WAV",
    "Fraktion der CDU/CSU (Gast)": "CDU/CSU",
    "Fraktion der Christlich Demokratischen Union/Christlich - Sozialen Union": "CDU/CSU",
    "Fraktion der FDP (Gast)": "FDP",
    "Fraktion der Freien Demokratischen Partei": "FDP",
    "Fraktion der Kommunistischen Partei Deutschlands": "KPD",
    "Fraktion der Partei des Demokratischen Sozialismus": "PDS",
    "Fraktion der SPD (Gast)": "SPD",
    "Fraktion der Sozialdemokratischen Partei Deutschlands": "SPD",
    "Fraktionslos": "Fraktionslos",
    "Gruppe Bündnis 90/Die Grünen": "Bündnis 90/Die Grünen",
    "Gruppe BSW - Bündnis Sahra Wagenknecht - Vernunft und Gerechtigkeit": "BSW",
    "Gruppe Deutsche Partei": "DP",
    "Gruppe Die Linke": "DIE LINKE.",
    "Gruppe Kraft/Oberländer": "KO",
    "Gruppe der Partei des Demokratischen Sozialismus": "PDS",
    "Gruppe der Partei des Demokratischen Sozialismus/Linke Liste": "PDS",
    "Südschleswigscher Wählerverband": "SSW",
    "Gast": "Gast",
    "Gruppe Nationale Rechte": "NR",
}

priority_factions = {
    "SPD": 1,
    "CDU/CSU": 2,
    "Bündnis 90/Die Grünen": 3,
    "FDP": 4,
    "DIE LINKE.": 5,
    "AfD": 6,
    "PDS": 7,
    "Fraktionslos": 99
}

factions.insert(0, "abbreviation", "")
factions["abbreviation"] = factions["faction_name"].apply(lambda x: abbreviations_dict[x])

#id spalte
factions.insert(0, "id", -1)

# Erste Priorität: Weise den wichtigen Fraktionen ihre festen IDs zu
for index, row in factions.iterrows():
    if row["abbreviation"] in priority_factions:
        factions.at[index, "id"] = priority_factions[row["abbreviation"]]

# Zweite Priorität: Weise restlichen Fraktionen fortlaufende IDs zu
next_id = max([v for v in priority_factions.values() if v < 99]) + 1  # Höchste ID +1, ignoriere Spezialwerte
for index, row in factions.iterrows():
    if row["id"] == -1:
        factions.at[index, "id"] = next_id
        next_id += 1


# save the dataframe
factions.to_pickle(DATA_FINAL / "factions.pkl")
