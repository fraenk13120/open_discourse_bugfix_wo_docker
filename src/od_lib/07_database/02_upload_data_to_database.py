import pandas as pd
import datetime
from od_lib.helper_functions.progressbar import progressbar


# Pfaddefinitionen
from od_lib.definitions import path_definitions

# Daten laden
electoral_terms = pd.read_csv(path_definitions.ELECTORAL_TERMS / "electoral_terms.csv")
politicians = pd.read_csv(path_definitions.DATA_FINAL / "politicians.csv")

# Politicians anpassen
politicians = politicians.drop_duplicates(subset=["ui"], keep="first")
politicians = politicians.drop([
    "electoral_term",
    "faction_id",
    "institution_type",
    "institution_name",
    "constituency",
], axis=1)
politicians.columns = [
    "id",
    "first_name",
    "last_name",
    "birth_place",
    "birth_country",
    "birth_date",
    "death_date",
    "gender",
    "profession",
    "aristocracy",
    "academic_title",
]

# Funktion zum Konvertieren von Daten
def convert_date_politicians(date):
    try:
        date = pd.to_datetime(date, format="%d.%m.%Y")
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        return date
    except (ValueError, TypeError):
        return None

def convert_date_speeches(date_value):
    try:
        if date_value is None:
            return None
        # Wenn date_value bereits ein datetime-Objekt ist
        if isinstance(date_value, datetime.datetime):
            return date_value.strftime("%Y-%m-%d %H:%M:%S")
        # Wenn es ein Unix-Timestamp ist (für Kompatibilität)
        return pd.to_datetime(date_value, unit='s').strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError) as e:
        print(f"Fehler bei Datumskonvertierung: {e}, Wert: {date_value}")
        return None

# Daten exportieren
# Beispiel für die Anpassung
def export_to_csv(data, filename):
    output_path = path_definitions.DATA / filename  # Anpassen auf deinen gewünschten Pfad
    try:
        data.to_csv(output_path, index=False)
        print(f"Daten erfolgreich in {output_path} geschrieben.")
    except Exception as e:
        print(f"Fehler beim Schreiben der Daten: {e}")


# Exportiere Daten
export_to_csv(electoral_terms, "electoral_terms.csv")
export_to_csv(politicians, "politicians.csv")

# Faktionen
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

try:
    factions_df = pd.read_pickle(path_definitions.DATA_FINAL / "factions.pkl")
    print(f"Factions aus Pickle geladen: {len(factions_df)} Einträge")
except Exception as e:
    print(f"Fehler beim Laden der Factions-Pickle: {e}")
    # Fallback zur manuellen Liste
factions = [[value, key] for key, value in abbreviations_dict.items()]

factions_df = pd.DataFrame(
    [[idx-1, *entry] for idx, entry in enumerate(factions)],
    columns=["id", "abbreviation", "full_name"],
)

# Stelle sicher, dass die richtigen Spalten vorhanden sind
if "faction_name" in factions_df.columns:
    factions_df = factions_df.rename(columns={"faction_name": "full_name"})

# Stelle sicher, dass die Spalten in der richtigen Reihenfolge sind
if "abbreviation" in factions_df.columns and "id" in factions_df.columns:
    factions_df = factions_df[["id", "abbreviation", "full_name"]]

factions_df["id"] = factions_df["id"].astype(int)
export_to_csv(factions_df, "factions.csv")

factions_df = pd.read_pickle(path_definitions.DATA_FINAL / "factions.pkl")
print(f"Anzahl der Fraktionen in der Pickle-Datei: {len(factions_df)}")

# Reden
speeches = pd.read_pickle(path_definitions.DATA_FINAL / "speech_content.pkl")
speeches["date"] = speeches["date"].apply(convert_date_speeches)
speeches["position_long"].replace([r"^\s*$"], [None], regex=True, inplace=True)
export_to_csv(speeches, "speeches.csv")

# Beiträge erweitert
contributions_extended = pd.read_pickle(path_definitions.DATA_FINAL / "contributions_extended.pkl")
export_to_csv(contributions_extended, "contributions_extended.csv")

# Beiträge vereinfacht
contributions_simplified = pd.read_pickle(path_definitions.CONTRIBUTIONS_SIMPLIFIED / "contributions_simplified.pkl")
export_to_csv(contributions_simplified, "contributions_simplified.csv")
