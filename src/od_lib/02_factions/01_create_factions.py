from od_lib.definitions import path_definitions
import pandas as pd
import numpy as np

# input directory
POLITICIANS_STAGE_01 = path_definitions.POLITICIANS_STAGE_01
# output directory
FACTIONS_STAGE_01 = path_definitions.FACTIONS_STAGE_01
FACTIONS_STAGE_01.mkdir(parents=True, exist_ok=True)

# read data.
mps = pd.read_pickle(POLITICIANS_STAGE_01 / "mps.pkl")

factions = mps.loc[mps["institution_type"] == "Fraktion/Gruppe", "institution_name"]

unique_factions = np.unique(factions)
unique_factions = np.append(
    unique_factions,
    [
        "Südschleswigscher Wählerverband",
        "Gast",
        "Gruppe Nationale Rechte",
        "Deutsche Soziale Union",
    ],
)
# Alle Fraktionen aus dem abbreviations_dict manuell hinzufügen
all_factions = [
    "Alternative für Deutschland",
    "Deutsche Soziale Union",
    "Fraktion Alternative für Deutschland",
    "Fraktion Bayernpartei",
    "Fraktion Bündnis 90/Die Grünen",
    "Fraktion DIE LINKE.",
    "Fraktion DP/DPB (Gast)",
    "Fraktion DRP (Gast)",
    "Fraktion Demokratische Arbeitsgemeinschaft",
    "Fraktion Deutsche Partei",
    "Fraktion Deutsche Partei Bayern",
    "Fraktion Deutsche Partei/Deutsche Partei Bayern",
    "Fraktion Deutsche Partei/Freie Volkspartei",
    "Fraktion Deutsche Reichspartei",
    "Fraktion Deutsche Reichspartei/Nationale Rechte",
    "Fraktion Deutsche Zentrums-Partei",
    "Fraktion Deutscher Gemeinschaftsblock der Heimatvertriebenen und Entrechteten",
    "Fraktion Die Grünen",
    "Fraktion Die Grünen/Bündnis 90",
    "Fraktion BÜNDNIS 90/DIE GRÜNEN",
    "Fraktion Freie Volkspartei",
    "Fraktion Föderalistische Union",
    "Fraktion Gesamtdeutscher Block / Block der Heimatvertriebenen und Entrechteten",
    "Fraktion WAV (Gast)",
    "Fraktion Wirtschaftliche Aufbauvereinigung",
    "Fraktion der CDU/CSU (Gast)",
    "Fraktion der Christlich Demokratischen Union/Christlich - Sozialen Union",
    "Fraktion der FDP (Gast)",
    "Fraktion der Freien Demokratischen Partei",
    "Fraktion der Kommunistischen Partei Deutschlands",
    "Fraktion der Partei des Demokratischen Sozialismus",
    "Fraktion der SPD (Gast)",
    "Fraktion der Sozialdemokratischen Partei Deutschlands",
    "Fraktionslos",
    "Gruppe Bündnis 90/Die Grünen",
    "Gruppe BSW - Bündnis Sahra Wagenknecht - Vernunft und Gerechtigkeit",
    "Gruppe Deutsche Partei",
    "Gruppe Die Linke",
    "Gruppe Kraft/Oberländer",
    "Gruppe der Partei des Demokratischen Sozialismus",
    "Gruppe der Partei des Demokratischen Sozialismus/Linke Liste",
    "Südschleswigscher Wählerverband",
    "Gast",
    "Gruppe Nationale Rechte"
]

# Kombiniere die extrahierten Fraktionen mit der manuellen Liste
unique_factions = np.unique(np.concatenate([factions, all_factions]))


unique_factions = pd.DataFrame(unique_factions, columns=["faction_name"])

save_path_factions = FACTIONS_STAGE_01 / "factions.pkl"
unique_factions.to_pickle(save_path_factions)
