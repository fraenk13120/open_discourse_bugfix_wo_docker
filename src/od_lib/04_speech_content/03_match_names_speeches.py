from od_lib.helper_functions.match_names import insert_politician_id_into_speech_content
from od_lib.definitions import path_definitions
from od_lib.helper_functions.progressbar import progressbar
import pandas as pd
import regex

# input directory
SPEECH_CONTENT_INPUT = path_definitions.SPEECH_CONTENT_STAGE_02
DATA_FINAL = path_definitions.DATA_FINAL

# output directory
SPEECH_CONTENT_OUTPUT = path_definitions.SPEECH_CONTENT_STAGE_03
SPEECH_CONTENT_OUTPUT.mkdir(parents=True, exist_ok=True)

# MDBS
politicians = pd.read_csv(DATA_FINAL / "politicians.csv")
politicians = politicians.loc[
    :,
    [
        "ui",
        "electoral_term",
        "faction_id",
        "first_name",
        "last_name",
        "gender",
        "profession",
        "constituency",
        "institution_type",
    ],
].copy()

politicians = politicians.astype(dtype={"ui": "int64"})

# Some cleaning to make matching easier.
# Konvertiere alle relevanten Spalten zu Strings
string_columns = ["first_name", "last_name", "constituency", "profession"]
for col in string_columns:
    politicians[col] = politicians[col].fillna("").astype(str)

# Dann führe die Transformationen durch
politicians["first_name"] = politicians["first_name"].str.lower()
politicians["last_name"] = politicians["last_name"].str.lower()
politicians["constituency"] = politicians["constituency"].str.lower()
politicians["profession"] = politicians["profession"].str.lower()
# usw.


politicians["constituency"] = politicians["constituency"].fillna("")

politicians["first_name"] = politicians["first_name"].str.lower()
politicians["last_name"] = politicians["last_name"].str.lower()
politicians["constituency"] = politicians["constituency"].str.lower()

politicians["first_name"] = politicians["first_name"].str.replace("ß", "ss", regex=False)
politicians["last_name"] = politicians["last_name"].str.replace("ß", "ss", regex=False)

politicians["first_name"] = politicians["first_name"].apply(str.split)

politicians["profession"] = politicians["profession"].str.lower()

# iterate over all electoral_term_folders __________________________________________________
for folder_path in sorted(SPEECH_CONTENT_INPUT.iterdir()):
    working = []
    if not folder_path.is_dir():
        continue

    term_number = regex.search(r"(?<=electoral_term_)\d{2}", folder_path.stem)
    if term_number is None:
        continue
    term_number = int(term_number.group(0))

    save_path = SPEECH_CONTENT_OUTPUT / folder_path.stem
    save_path.mkdir(parents=True, exist_ok=True)

    # Only select politicians of the election period.
    politicians_electoral_term = politicians.loc[
        politicians["electoral_term"] == term_number
    ]
    mgs_electoral_term = politicians_electoral_term.loc[
        politicians_electoral_term["institution_type"] == "Regierungsmitglied"
    ]

    # iterate over every speech_content file
    for speech_content_file in progressbar(
        folder_path.glob("*.pkl"),
        f"Match speaker names (term {term_number:>2})..."
    ):
        # read the spoken content pickle file
        speech_content = pd.read_pickle(speech_content_file)

        speech_content_matched, _ = insert_politician_id_into_speech_content(
            speech_content, politicians_electoral_term, mgs_electoral_term, politicians
        )
        for index, row in speech_content_matched.iterrows():
            if row["politician_id"] != -1:
                # Finde den zugehörigen Politiker
                politician = politicians[politicians["ui"] == row["politician_id"]]
                if not politician.empty:
                    # Übernehme die Fraktions-ID, wenn vorhanden
                    faction_id = politician["faction_id"].iloc[0]
                    if faction_id != -1:
                        speech_content_matched.at[index, "faction_id"] = faction_id

        speech_content_matched.to_pickle(save_path / speech_content_file.name)
