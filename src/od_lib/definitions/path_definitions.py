from pathlib import Path

# Basisverzeichnis dynamisch ermitteln
PROJECT_ROOT = Path(__file__).resolve().parents[3]  # Anpassung je nach Struktur

# Hauptverzeichnisse
DATA = PROJECT_ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

SRC = PROJECT_ROOT / "src"

# Raw Data-Strukturen
DATA_RAW = DATA / "01_raw"
DATA_RAW.mkdir(exist_ok=True)

RAW_XML = DATA_RAW / "xml"


# Text-Verzeichnis
RAW_TXT = DATA_RAW / "txt"
RAW_TXT.mkdir(parents=True, exist_ok=True)

# Verarbeitungsstufen
DATA_CACHE = DATA / "02_cached"
DATA_FINAL = DATA / "03_final"

#Factions
FACTIONS = DATA_CACHE / "factions"
FACTIONS_STAGE_01 = FACTIONS / "stage_01"
FACTIONS_STAGE_01.mkdir(parents=True, exist_ok=True)
FACTIONS_STAGE_02 = FACTIONS / "stage_02"
FACTIONS_STAGE_02.mkdir(parents=True, exist_ok=True)
FACTIONS_FINAL = FACTIONS / "final"
FACTIONS_FINAL.mkdir(parents=True, exist_ok=True)

FINAL = DATA_FINAL

# CONTRIBUTIONS_SIMPLIFIED _________________________________________________________________________
CONTRIBUTIONS_SIMPLIFIED = FINAL

# ELECTORAL_TERMS __________________________________________________________________________________
ELECTORAL_TERMS = FINAL

#Terms
ELECTORAL_TERMS = DATA_FINAL / "electoral_terms"

ELECTORAL_TERMS.mkdir(parents=True, exist_ok=True)

# Politikerdaten
MP_BASE_DATA = DATA_RAW / "MP_BASE_DATA" / "MDB_STAMMDATEN.XML"
POLITICIANS = DATA_CACHE / "politicians"
POLITICIANS_STAGE_01 = POLITICIANS / "stage_01"
POLITICIANS_STAGE_01.mkdir(parents=True, exist_ok=True)
POLITICIANS_STAGE_02 = POLITICIANS / "stage_02"
POLITICIANS_STAGE_02.mkdir(parents=True, exist_ok=True)
POLITICIANS_FINAL = POLITICIANS / "final"
POLITICIANS_FINAL.mkdir(parents=True, exist_ok=True)

# SPEECH CONTENT ___________________________________________________________________________________
SPEECH_CONTENT = DATA_CACHE / "speech_content"
SPEECH_CONTENT_STAGE_01 = SPEECH_CONTENT / "stage_01"
SPEECH_CONTENT_STAGE_02 = SPEECH_CONTENT / "stage_02"
SPEECH_CONTENT_STAGE_03 = SPEECH_CONTENT / "stage_03"
SPEECH_CONTENT_STAGE_04 = SPEECH_CONTENT / "stage_04"
SPEECH_CONTENT_FINAL = SPEECH_CONTENT / "final"

# CONTRIBUTIONS_EXTENDED ___________________________________________________________________________
CONTRIBUTIONS_EXTENDED = DATA_CACHE / "contributions_extended"
CONTRIBUTIONS_EXTENDED_STAGE_01 = CONTRIBUTIONS_EXTENDED / "stage_01"
CONTRIBUTIONS_EXTENDED_STAGE_02 = CONTRIBUTIONS_EXTENDED / "stage_02"
CONTRIBUTIONS_EXTENDED_STAGE_03 = CONTRIBUTIONS_EXTENDED / "stage_03"
CONTRIBUTIONS_EXTENDED_STAGE_04 = CONTRIBUTIONS_EXTENDED / "stage_04"

CONTRIBUTIONS_EXTENDED_FINAL = CONTRIBUTIONS_EXTENDED / "final"

