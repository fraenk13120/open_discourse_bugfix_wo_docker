from od_lib.definitions import path_definitions
import pandas as pd
import difflib


# input directory
POLITICIANS_INPUT = path_definitions.POLITICIANS_STAGE_01
FACTIONS_INPUT = path_definitions.DATA_FINAL
# output directory
POLITICIANS_OUTPUT = path_definitions.POLITICIANS_STAGE_02
POLITICIANS_OUTPUT.mkdir(parents=True, exist_ok=True)

factions = pd.read_pickle(FACTIONS_INPUT / "factions.pkl")
mps = pd.read_pickle(POLITICIANS_INPUT / "mps.pkl")

mps.insert(2, "faction_id", -1)

# Prüfe, welche Spalten in der Fraktions-Datei vorhanden sind
print(f"Spalten in factions: {factions.columns.tolist()}")

# Verwende die richtige Spalte für den Fraktionsnamen
faction_name_column = "faction_name" if "faction_name" in factions.columns else "full_name"

# Exakte Übereinstimmung
for faction_name, faction_id in zip(factions[faction_name_column], factions["id"]):
    mps.loc[mps["institution_name"] == faction_name, "faction_id"] = faction_id

# Fuzzy-Matching für nicht zugeordnete Politiker
unassigned_mps = mps[mps["faction_id"] == -1]
for index, row in unassigned_mps.iterrows():
    institution_name = row["institution_name"]
    
    # Teilstring-Matching
    for faction_name, faction_id in zip(factions[faction_name_column], factions["id"]):
        if faction_name in institution_name or institution_name in faction_name:
            mps.at[index, "faction_id"] = faction_id
            break
    
    # Wenn immer noch nicht zugeordnet, versuche Fuzzy-Matching
    if mps.at[index, "faction_id"] == -1:
        matches = difflib.get_close_matches(institution_name, factions[faction_name_column].tolist(), n=1, cutoff=0.7)
        if matches:
            faction_id = factions[factions[faction_name_column] == matches[0]].iloc[0]["id"]
            mps.at[index, "faction_id"] = faction_id

mps.to_pickle(POLITICIANS_OUTPUT / "mps.pkl")
