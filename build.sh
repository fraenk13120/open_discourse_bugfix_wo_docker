#!/bin/bash

# Aktiviere die virtuelle Umgebung
# source ./.venv/Scripts/activate


# Erstelle Log-Verzeichnis
mkdir -p logs

python_exe="python"

# Pfade definieren
src_path=src/od_lib
preprocessing_path=$src_path/01_preprocessing
factions_path=$src_path/02_factions
politicians_path=$src_path/03_politicians
speech_content_path=$src_path/04_speech_content
contributions_path=$src_path/06_contributions
database_path=$src_path/07_database

# Führe die Datenverarbeitungsskripte aus
$python_exe $preprocessing_path/01_download_raw_data.py 2>&1 | tee logs/01_download_raw_data_log.log
$python_exe $preprocessing_path/02_download_raw_data_electoral_term_19_20.py 2>&1 | tee logs/02_download_raw_data_electoral_term_19_20_log.log
$python_exe $preprocessing_path/03_split_xml.py 2>&1 | tee logs/03_split_xml_log.log
$python_exe $preprocessing_path/04_split_xml_electoral_term_1_and_2.py 2>&1 | tee logs/04_split_xml_electoral_term_1_and_2_log.log
$python_exe $preprocessing_path/06_extract_mps_from_mp_base_data.py 2>&1 | tee logs/06_extract_mps_from_mp_base_data_log.log
$python_exe $preprocessing_path/07_create_electoral_terms.py 2>&1 | tee logs/07_create_electoral_terms_log.log
$python_exe $factions_path/01_create_factions.py 2>&1 | tee logs/01_create_factions_log.log
$python_exe $factions_path/02_add_abbreviations_and_ids.py 2>&1 | tee logs/02_add_abbreviations_and_ids_log.log
$python_exe $politicians_path/01_add_faction_id_to_mps.py 2>&1 | tee logs/01_add_faction_id_to_mps_log.log
$python_exe $politicians_path/02_scrape_mgs.py 2>&1 | tee logs/02_scrape_mgs_log.log
$python_exe $politicians_path/03_merge_politicians.py 2>&1 | tee logs/03_merge_politicians_log.log
$python_exe $speech_content_path/01_extract_speeches.py 2>&1 | tee logs/01_extract_speeches_log.log
$python_exe $speech_content_path/02_clean_speeches.py 2>&1 | tee logs/02_clean_speeches.log
$python_exe $speech_content_path/03_match_names_speeches.py 2>&1 | tee logs/03_match_names_speeches_log.log
$python_exe $contributions_path/01_extract_contributions.py 2>&1 | tee logs/01_extract_contributions_log.log
$python_exe $contributions_path/02_clean_contributions_extended.py 2>&1 | tee logs/02_clean_contributions_extended_log.log
$python_exe $contributions_path/03_match_contributions_extended.py 2>&1 | tee logs/03_match_contributions_extended_log.log
$python_exe $database_path/01_concat_everything.py 2>&1 | tee logs/01_concat_everything_log.log

# Exportiere Daten in CSV-Dateien (statt in die Datenbank)
$python_exe $database_path/02_upload_data_to_database.py 2>&1 | tee logs/02_upload_data_to_database_log.log
