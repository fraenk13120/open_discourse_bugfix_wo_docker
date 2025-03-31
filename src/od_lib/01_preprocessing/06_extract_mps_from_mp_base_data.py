from od_lib.definitions import path_definitions
import pandas as pd
import xml.etree.ElementTree as et
import regex
import os

# input directory
MP_BASE_DATA = path_definitions.MP_BASE_DATA

# output directory
POLITICIANS_STAGE_01 = path_definitions.POLITICIANS_STAGE_01
POLITICIANS_STAGE_01.mkdir(parents=True, exist_ok=True)

save_path = POLITICIANS_STAGE_01 / "mps.pkl"

print("Process mps...", end="", flush=True)

# Überprüfen, ob die Datei existiert
if not os.path.exists(MP_BASE_DATA):
    print(f"FEHLER: Die Datei {MP_BASE_DATA} existiert nicht!")
    exit(1)

# read data
tree = et.parse(MP_BASE_DATA)
root = tree.getroot()

print(f"XML-Datei gefunden: {MP_BASE_DATA}")
print(f"Root-Element: {root.tag}")

# placeholder for final dataframe
mps = {
    "ui": [],
    "electoral_term": [],
    "first_name": [],
    "last_name": [],
    "birth_place": [],
    "birth_country": [],
    "birth_date": [],
    "death_date": [],
    "gender": [],
    "profession": [],
    "constituency": [],
    "aristocracy": [],
    "academic_title": [],
    "institution_type": [],
    "institution_name": [],
}

# Iterate over all document elements in XML File
for document in root.findall("./document"):
    # Extrahiere die Daten aus der neuen XML-Struktur
    ui = document.findtext("id")
    if not ui:
        continue
        
    last_name = document.findtext("nachname")
    first_name = document.findtext("vorname")
    electoral_term = document.findtext("wahlperiode")
    
    # Extrahiere Fraktionsinformationen
    person_roles = document.find("person_roles")
    if person_roles is not None:
        institution_type = person_roles.findtext("funktion") or ""
        institution_name = person_roles.findtext("fraktion") or ""
    else:
        institution_type = ""
        institution_name = ""
    
    # Setze Standardwerte für fehlende Felder
    birth_place = ""
    birth_country = "Deutschland"  # Annahme
    birth_date = ""
    death_date = "-1"
    gender = ""
    profession = ""
    constituency = ""
    aristocracy = ""
    academic_title = ""
    
    # Extrahiere akademischen Titel aus dem Gesamttitel, wenn vorhanden
    titel = document.findtext("titel") or ""
    if "Dr." in titel:
        academic_title = "Dr."
    
    # Füge die Daten zum DataFrame hinzu
    mps["ui"].append(ui)
    mps["electoral_term"].append(electoral_term)
    mps["first_name"].append(first_name)
    mps["last_name"].append(last_name)
    mps["birth_place"].append(birth_place)
    mps["birth_country"].append(birth_country)
    mps["birth_date"].append(birth_date)
    mps["death_date"].append(death_date)
    mps["gender"].append(gender)
    mps["profession"].append(profession)
    mps["constituency"].append(constituency)
    mps["aristocracy"].append(aristocracy)
    mps["academic_title"].append(academic_title)
    mps["institution_type"].append(institution_type)
    mps["institution_name"].append(institution_name)

mps = pd.DataFrame(mps)

# spalte explizit zu String
mps["constituency"] = mps["constituency"].astype(str)
mps["constituency"] = mps["constituency"].str.replace("[)(]", "", regex=True)

# Konvertiere Datentypen
mps = mps.astype(dtype={"ui": "int64", "birth_date": "str", "death_date": "str"})

mps.to_pickle(save_path)

print("Done.")
print(f"Anzahl der extrahierten Datensätze: {len(mps)}")
