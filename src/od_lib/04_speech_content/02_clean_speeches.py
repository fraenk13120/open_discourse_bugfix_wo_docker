from od_lib.helper_functions.clean_text import clean_name_headers
from od_lib.definitions import path_definitions
from od_lib.helper_functions.progressbar import progressbar
import numpy as np
import pandas as pd
import sys
import regex
import difflib

# input directory
SPEECH_CONTENT_INPUT = path_definitions.SPEECH_CONTENT_STAGE_01
FACTIONS = path_definitions.DATA_FINAL

# output directory
SPEECH_CONTENT_OUTPUT = path_definitions.SPEECH_CONTENT_STAGE_02

factions = pd.read_pickle(FACTIONS / "factions.pkl")

faction_patterns = {
    "Bündnis 90/Die Grünen": r"(?:BÜNDNIS\s*(?:90)?/?(?:\s*D[1I]E)?|Bündnis\s*90/(?:\s*D[1I]E)?)?\s*[GC]R[UÜ].?\s*[ÑN]EN?(?:/Bündnis 90)?|Bündnis 90/Die Grünen",  # noqa: E501
    "CDU/CSU": r"(?:Gast|-)?(?:\s*C\s*[DSMU]\s*S?[DU]\s*(?:\s*[/,':!.-]?)*\s*(?:\s*C+\s*[DSs]?\s*[UÙ]?\s*)?)(?:-?Hosp\.|-Gast|1)?",  # noqa: E501
    "BP": r"^BP",
    "DA": r"^DA",
    "DP": r"^DP",
    "DIE LINKE.": r"DIE LINKE",
    "DPB": r"(?:^DPB)",
    "DRP": r"DRP(\-Hosp\.)?|SRP",
    "FDP": r"\s*F\.?\s*[PDO][.']?[DP]\.?",
    "Fraktionslos": r"(?:fraktionslos|Parteilos|parteilos)",
    "FU": r"^FU",
    "FVP": r"^FVP",
    "Gast": r"Gast",
    "GB/BHE": r"(?:GB[/-]\s*)?BHE(?:-DG)?",
    "KPD": r"^KPD",
    "PDS": r"(?:Gruppe\s*der\s*)?PDS(?:/(?:LL|Linke Liste))?",
    "SPD": r"\s*'?S(?:PD|DP)(?:\.|-Gast)?",
    "SSW": r"^SSW",
    "SRP": r"^SRP",
    "WAV": r"^WAV",
    "Z": r"^Z$",
    "DBP": r"^DBP$",
    "NR": r"^NR$",
}

def get_faction_abbrev(faction, faction_patterns):
    """matches the given faction and returns an id"""
    import difflib  # Import hinzufügen falls nicht bereits am Anfang der Datei vorhanden
    
    faction = str(faction).strip()
    faction = regex.sub(r'\s+', ' ', faction)
    
    # Direkte Übereinstimmung prüfen
    for faction_abbrev, faction_pattern in faction_patterns.items():
        if regex.search(faction_pattern, faction, regex.IGNORECASE):
            return faction_abbrev
    
    # Wenn keine direkte Übereinstimmung, versuche Teilstring-Matching
    for faction_abbrev, faction_pattern in faction_patterns.items():
        pattern_text = regex.sub(r'[\\^$.|?*+()]', '', faction_pattern)
        if pattern_text in faction or faction in pattern_text:
            return faction_abbrev
            
    # Füge Fuzzy-Matching als letzten Ausweg hinzu
    best_match = None
    best_ratio = 0
    threshold = 0.7  # Niedrigerer Schwellenwert
    
    for faction_abbrev in faction_patterns.keys():
        # Vergleiche den Fraktionsnamen direkt mit der Abkürzung
        ratio = difflib.SequenceMatcher(None, faction.lower(), faction_abbrev.lower()).ratio()
        if ratio > best_ratio:
            best_match = faction_abbrev
            best_ratio = ratio
    
    return best_match if best_ratio > threshold else None



def get_position_short_and_long(position):
    """matches the given position and returns the long and short version"""
    if position in faction_patterns.keys() or regex.match(
        r"^[Bb]erichterstatter(in)?(\s|$|,|.)", position
    ):
        return (
            "Member of Parliament",
            None if position in faction_patterns.keys() else position,
        )
    elif (
        regex.match(r"^[Bb]undestagspräsident(in)?(\s|$|,|.)", position)
        or regex.match(r"^[Aa]lterspräsident(in)?(\s|$|,|.)", position)
        or regex.match(r"^[Vv]izebundestagspräsident(in)?(\s|$|,|.)", position)
        or regex.match(r"^[Ss]chriftführer(in)?(\s|$|,|.)", position)
        or position.lower()
        in [
            "präsidentin",
            "präsident",
            "präsident des deutschen bundestages",
            "präsidentin des deutschen bundestages",
            "vizepräsidentin",
            "vizepräsident",
        ]
    ):
        return "Presidium of Parliament", position
    elif (
        regex.match(r"^[Bb]undespräsident(in)?(\s|$|,|.)", position)
        or regex.match(r"^[Ss]taatsminister(in)?(\s|$|,|.)", position)
        or regex.match(r"^[Ss]enator(in)?(\s|$|,|.)", position)
        or regex.match(r"^[Pp]räsident(in)?(\s|$|,|.)", position)
        or regex.match(r"^[Gg]ast", position)
    ):
        return "Guest", position
    elif regex.match(r"^[Bb]undeskanzler(in)?(\s|$|,|.)", position):
        return "Chancellor", None
    elif regex.match(r"^(Bundes)?[Mm]inister(in)?(\s|$|,|.)", position):
        return "Minister", position
    elif regex.match(r"^([Pp]arl\s*\.\s+)?[Ss]taatssekretär(in)?(\s|$|,|.)", position):
        return "Secretary of State", position
    else:
        return "Not found", None


# iterate over all electoral_term_folders
for folder_path in sorted(SPEECH_CONTENT_INPUT.iterdir()):
    if not folder_path.is_dir():
        continue

    term_number = regex.search(r"(?<=electoral_term_)\d{2}", folder_path.stem)
    if term_number is None:
        continue
    term_number = int(term_number.group(0))

    if len(sys.argv) > 1:
        if str(term_number) not in sys.argv:
            continue

    save_path = SPEECH_CONTENT_OUTPUT / folder_path.stem
    save_path.mkdir(parents=True, exist_ok=True)

    # iterate over every speech_content file
    for speech_content_file in progressbar(
        folder_path.glob("*.pkl"),
        f"Clean speeches (term {term_number:>2})...",
    ):
        # read the spoken content csv
        speech_content = pd.read_pickle(speech_content_file)

        # Insert acad_title column and extract plain name and titles.
        # ADD DOCUMENTATION HERE
        speech_content.insert(3, "faction_id", -1)
        speech_content.insert(3, "position_short", "")
        speech_content.insert(4, "position_long", "")
        speech_content.insert(5, "last_name", "")
        speech_content.insert(6, "first_name", "")
        speech_content.insert(7, "acad_title", "")

        # Current workaround, because some speeches seem to not be matched
        # correctly. If second stage works without mistakes (extracting the
        # speech parts), this should not be necessary anymore.
        speech_content = speech_content.fillna("")

        # Clean all the names still remaining from PDF Header.
        # KEEP IN MIND THIS ALSO DELETES NAMES IN VOTING LISTS!!!
        # And I think not all names are cleaned because of their position, e.g.
        # "Max Mustermann, Bundeskanzler"
        # THIS PART IS IMPORTANT AND SHOULD WORK PROPERLY, AS REOCCURING NAMES
        # CAN INTRODUCE A LARGE BIAS IN TEXT ANALYSIS
        names = speech_content["name_raw"].to_list()
        speech_content["speech_content"] = speech_content["speech_content"].apply(
            clean_name_headers, args=(np.unique(names),)
        )

        speech_content.reset_index(inplace=True, drop=True)

        # Delete all not alphabetical chars, keep "-" as it occurs often in
        # names.
        # Question: Is any other character deleted, which could be in a name?
        # Answer: I don't think so.
        speech_content["name_raw"] = speech_content["name_raw"].str.replace(
            r"[^a-zA-ZÖÄÜäöüß\-]", " ", regex=True
        )

        # Replace more than two whitespaces with one.
        speech_content["name_raw"] = speech_content["name_raw"].str.replace(
            r"  +", " ", regex=True
        )

        # Graf has to be checked again, as this is also a last_name.
        # Titles have to be added: Like e.c. or when mistakes occur like b.c.
        # Deleted "Graf" for now.
        titles = [
            "Dr",
            "Frau",
            "D",
            "-Ing",
            "von",
            "und",
            "zu",
            "van",
            "de",
            "Baron",
            "Freiherr",
            "Prinz",
            "h",
            "c",
        ]

        # Split the name column into it's components at space character.
        first_last_titles = speech_content["name_raw"].apply(str.split)

        # Extract acad_title, if it is in the titles list.
        speech_content["acad_title"] = [
            [acad_title for acad_title in title_list if acad_title in titles]
            for title_list in first_last_titles
        ]

        # Remove titles from the first_last_name list.
        for politician_titles in first_last_titles:
            for acad_title in politician_titles[:]:
                if acad_title in titles:
                    politician_titles.remove(acad_title)

        # Get the first and last name based on the amount of elements.
        for index, first_last in first_last_titles.items():
            if len(first_last) == 1:
                speech_content.at[index, "first_name"] = ""
                speech_content.at[index, "last_name"] = first_last[0]
            elif len(first_last) >= 2:
                speech_content.at[index, "first_name"] = first_last[:-1]
                speech_content.at[index, "last_name"] = first_last[-1]
            else:
                speech_content.at[index, "first_name"] = "ERROR"
                speech_content.at[index, "last_name"] = "ERROR"

        # look for factions in the faction column and replace them with a
        # standardized faction name
        for index, position_raw in speech_content["position_raw"].items():
            faction_abbrev = get_faction_abbrev(str(position_raw), faction_patterns)
            (
                speech_content.at[index, "position_short"],
                speech_content.at[index, "position_long"],
            ) = get_position_short_and_long(
                faction_abbrev if faction_abbrev else regex.sub("\n+", " ", position_raw)
            )
            if faction_abbrev:
                try:
                    speech_content.at[index, "faction_id"] = int(
                        factions.loc[factions["abbreviation"] == faction_abbrev, "id"].iloc[0]
                    )
                except IndexError:
                    speech_content.at[index, "faction_id"] = -1

        speech_content = speech_content.drop(columns=["position_raw", "name_raw"])
        speech_content.to_pickle(save_path / speech_content_file.name)
