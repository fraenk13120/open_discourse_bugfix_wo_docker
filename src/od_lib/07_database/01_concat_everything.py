from od_lib.definitions import path_definitions
import xml.etree.ElementTree as et
import pandas as pd
import regex
import time
import datetime
import sys
from od_lib.helper_functions.progressbar import progressbar


# input directory
RAW_XML = path_definitions.RAW_XML
SPEECH_CONTENT_INPUT = path_definitions.SPEECH_CONTENT_STAGE_04

CONTRIBUTIONS_EXTENDED_INPUT = path_definitions.CONTRIBUTIONS_EXTENDED_STAGE_03

# output directory
SPEECH_CONTENT_OUTPUT = path_definitions.FINAL
CONTRIBUTIONS_EXTENDED_OUTPUT = path_definitions.FINAL

SPEECH_CONTENT_OUTPUT.mkdir(parents=True, exist_ok=True)
CONTRIBUTIONS_EXTENDED_OUTPUT.mkdir(parents=True, exist_ok=True)

# spoken content

# Placeholder for concating speeches DF of all sessions.
speech_content_01_19 = []


# Walk over all legislature periods.
for folder_path in sorted(SPEECH_CONTENT_INPUT.iterdir()):
    if not folder_path.is_dir():
        continue

    for speech_content_file_path in sorted(folder_path.glob("*.pkl")):
        speech_content_01_19.append(pd.read_pickle(speech_content_file_path))

speech_content_01_19 = pd.concat(speech_content_01_19, sort=False)

speech_content_01_19 = speech_content_01_19.loc[
    :,
    [
        "speech_id",
        "session",
        "first_name",
        "last_name",
        "faction_id",
        "position_short",
        "position_long",
        "politician_id",
        "speech_content",
    ],
]

speech_content_01_19 = speech_content_01_19.rename(columns={"speech_id": "id"})


speech_content_01_19["first_name"] = speech_content_01_19["first_name"].apply(" ".join)

speech_content_01_19["id"] = list(range(len(speech_content_01_19)))

speech_content_01_19["session"] = speech_content_01_19["session"].str.replace(
    r"\.pkl", "", regex=True
)


meta_data = {}

def safe_date_conversion(date_str):
    try:
        # Parsen des Datums
        dt = datetime.datetime.strptime(date_str, "%d.%m.%Y")
        # unix führt zu Problemen vor 1970
        # als ISO-Format oder als datetime-Objekt
        return dt
    except (ValueError, TypeError):
        print(f"Problematisches Datum: {date_str}")
        return None

xml_files = []

# Open every xml plenar file in every legislature period.
for folder_path in sorted(RAW_XML.iterdir()):
    # Skip e.g. the .DS_Store file.
    if not folder_path.is_dir():
        continue

    term_number = regex.search(r"(?<=electoral_term_)\d{2}", folder_path.stem)
    if term_number is None:
        continue
    term_number = int(term_number.group(0))

    if len(sys.argv) > 1:
        if str(term_number) not in sys.argv:
            continue
    
    xml_files.extend(sorted(folder_path.glob("*.xml")))

    print("Verarbeite XML-Dateien...")

    for i, xml_plenar_file_path in enumerate(progressbar(xml_files)):
        tree = et.parse(xml_plenar_file_path)
        # Get the document number, the date of the session and the content.
        # meta_data["document_number"].append(tree.find("NR").text)
        # meta_data["date"].append(tree.find("DATUM").text)
        # document_number = tree.find("NR").text
        date_text = tree.find("DATUM").text
        date_obj = safe_date_conversion(date_text)
        document_number = xml_plenar_file_path.stem
        document_number = int(document_number)
        if date_obj is not None:
            meta_data[document_number] = date_obj

speech_content_01_19.insert(1, "electoral_term", -1)
speech_content_01_19.insert(4, "document_url", "")
speech_content_01_19["electoral_term"] = speech_content_01_19["session"].apply(
    lambda x: str(x)[:2]
)
speech_content_01_19["session"] = speech_content_01_19["session"].astype("int32")
speech_content_01_19["date"] = speech_content_01_19["session"].apply(
    lambda x: meta_data.get(x)
)
speech_content_01_19["session"] = speech_content_01_19["session"].apply(
    lambda x: str(x)[-3:]
)

speech_content_01_19["document_url"] = speech_content_01_19.apply(
    lambda row: "https://dip21.bundestag.de/dip21/btp/{0}/{0}{1}.pdf".format(
        row["electoral_term"], row["session"]
    ),
    axis=1,
)

speech_content_01_19["session"] = speech_content_01_19["session"].astype("int32")
speech_content_01_19["electoral_term"].astype(
    "int32"
)







# save data.

speech_content_01_19.to_pickle(SPEECH_CONTENT_OUTPUT / "speech_content.pkl")

# Placeholder for concating contributions_extended DF of all sessions.
contributions_extended = []
contrib_files = []

# Walk over all legislature periods. ___________________________________________
for folder_path in sorted(CONTRIBUTIONS_EXTENDED_INPUT.iterdir()):
    # Skip e.g. the .DS_Store file.
    if not folder_path.is_dir():
        continue

    term_number = regex.search(r"(?<=electoral_term_)\d{2}", folder_path.stem)
    if term_number is None:
        continue
    term_number = int(term_number.group(0))

    if term_number == 19:
        print(f"Überspringe Wahlperiode 19")
        continue

    contrib_files.extend(sorted(folder_path.glob("*.pkl")))
    
print("Verarbeite Contributions-Dateien...")

for i, contrib_ext_file_path in enumerate(progressbar(contrib_files)):
    contributions_extended.append(pd.read_pickle(contrib_ext_file_path))

if contributions_extended:
    contributions_extended = pd.concat(contributions_extended, sort=False)
    # Rest des Codes...
else:
    print("Warnung: Keine Contributions-Dateien gefunden oder geladen!")
    # Erstelle einen leeren DataFrame mit der richtigen Struktur
    contributions_extended = pd.DataFrame(columns=[
        "type", "first_name", "last_name", "faction_id", 
        "id", "text_position", "politician_id", "content"
    ])


contributions_extended = contributions_extended.loc[
    :,
    [
        "type",
        "first_name",
        "last_name",
        "faction_id",
        "id",
        "text_position",
        "politician_id",
        "content",
    ],
]

contributions_extended = contributions_extended.rename(
    columns={"id": "speech_id", "politician_id": "politician_id"}
)

contributions_extended.insert(
    0, "id", list(range(len(contributions_extended)))
)

contributions_extended["first_name"] = (
    contributions_extended["first_name"].apply(" ".join)
)

contributions_extended = contributions_extended.astype(
    {
        "id": "int64",
        "type": "object",
        "first_name": "object",
        "last_name": "object",
        "faction_id": "int32",
        "speech_id": "int32",
        "text_position": "int32",
        "politician_id": "int32",
        "content": "object",
    }
)

contributions_extended.to_pickle(
    CONTRIBUTIONS_EXTENDED_OUTPUT / "contributions_extended.pkl"
)
