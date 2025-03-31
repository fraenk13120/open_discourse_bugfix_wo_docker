import sys
import os
import requests
import zipfile
import io
from datetime import datetime
import time
from od_lib.definitions import path_definitions


# API-Konfiguration
API_KEY = "I9FKdCn.hbfefNWCY336dL6x62vfwNKpoN2RZ1gp21"
HEADERS = {
    "Authorization": f"ApiKey {API_KEY}",
    "Accept": "application/json"
}

MAX_RETRIES = 3
TIMEOUT = 30

# Liste der URLs für jede Wahlperiode
wp_urls = {
    1: "https://www.bundestag.de/resource/blob/487966/4078f01fb3198dc3cee8945d6db3b231/pp01.zip",
    2: "https://www.bundestag.de/resource/blob/487968/5792895a5cf4ab51ed94c77157297031/pp02.zip",
    3: "https://www.bundestag.de/resource/blob/487970/1c737594587745b399e84bc30f049d69/pp03.zip",
    4: "https://www.bundestag.de/resource/blob/488216/3b20f8dd5efad2cafa3fb0b6df24cbb9/pp04.zip",
    5: "https://www.bundestag.de/resource/blob/488218/bfba1a02d1090efc873f9a60f318a162/pp05.zip",
    6: "https://www.bundestag.de/resource/blob/488220/b2b4d0d49600ef852d15e4052fabce1e/pp06.zip",
    7: "https://www.bundestag.de/resource/blob/488222/b10bae395e887aac9ac08afbd1da62fc/pp07.zip",
    8: "https://www.bundestag.de/resource/blob/490390/dfcac024ce8e548774e16f03c36293e2/pp08.zip",
    9: "https://www.bundestag.de/resource/blob/490382/effcc03f3b3e157f9d8050b4a9d9d089/pp09.zip",
    10: "https://www.bundestag.de/resource/blob/490374/07ce06f666b624d37b47d2fe6e205ab4/pp10.zip",
    11: "https://www.bundestag.de/resource/blob/490384/ad57841a599aba6faa794174e53a8797/pp11.zip",
    12: "https://www.bundestag.de/resource/blob/490376/8775517464dccd8660eb96446d18dd26/pp12.zip",
    13: "https://www.bundestag.de/resource/blob/490388/84914a1feff6f2f4988ce352a5500845/pp13.zip",
    14: "https://www.bundestag.de/resource/blob/490380/c4ca5488b447668f802039f1f769b278/pp14.zip",
    15: "https://www.bundestag.de/resource/blob/490394/08411d0257e9e07daef24001a958db53/pp15.zip",
    16: "https://www.bundestag.de/resource/blob/490386/80886372e6bbe903dd4d7eb03fe424b3/pp16.zip",
    17: "https://www.bundestag.de/resource/blob/490378/033276846771aac12dd7109724a1134b/pp17.zip",
    18: "https://www.bundestag.de/resource/blob/490392/90738376bb195628b95d117ab5392cfe/pp18.zip",
    19: "https://www.bundestag.de/resource/blob/870686/91b713c492499db98eec5b2f8f142d20/pp19.zip"
}

def fetch_plenary_protocols(wp_start, wp_end):
    """Holt Protokolle direkt über die angegebenen URLs"""
    for wp in range(wp_start, wp_end + 1):
        print(f"\n{'='*30}\nVerarbeite Wahlperiode {wp}\n{'='*30}")
        
        zip_url = wp_urls[wp]
        
        electoral_term_str = f"electoral_term_{wp:02d}"
        save_path = path_definitions.RAW_XML / electoral_term_str
        save_path.mkdir(parents=True, exist_ok=True)

        try:
            with requests.Session() as session:
                session.mount('https://', HTTPAdapter(max_retries=3))
                response = session.get(zip_url, headers=HEADERS, timeout=45)

                if response.status_code != 200:
                    raise ValueError(f"HTTP {response.status_code} - {response.text[:200]}")

                if 'application/zip' not in response.headers.get('Content-Type', ''):
                    raise ValueError("Invalid content type - not a ZIP file")

                try:
                    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                        if z.testzip() is not None:
                            raise zipfile.BadZipFile("Corrupt ZIP structure")
                        z.extractall(save_path)
                except zipfile.BadZipFile as e:
                    print(f"⨯ FEHLER WP {wp}: {str(e)}")
                    print(f"Manueller Check: {zip_url}")
                    with open(os.path.join(save_path, f"wp{wp}_error.zip"), 'wb') as f:
                        f.write(response.content)

                print(f"✓ Wahlperiode {wp} heruntergeladen")

        except Exception as e:
            print(f"\n⨯ FEHLER WP {wp}: {str(e)}")
            print(f"Manueller Check: {zip_url}")

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

# Hauptausführung
if __name__ == "__main__":
    # Historische Daten (WP 1-19)
    fetch_plenary_protocols(1, 19)


    # MDB-Stammdaten
    print("\nDownload MP_BASE_DATA...")
    try:
        mp_params = {
            "format": "xml",
            "f.zuordnung": "BT",
            "cursor": "*"
        }
        
        mp_url = "https://search.dip.bundestag.de/api/v1/person"
        # Erstelle eine neue Sitzung
        with requests.Session() as session:
            session.headers.update(HEADERS)
            response = session.get(mp_url, params=mp_params)
            response.raise_for_status()
            
            mp_base_data_dir = path_definitions.MP_BASE_DATA.parent
            mp_base_data_dir.mkdir(parents=True, exist_ok=True)
            # Die API liefert wahrscheinlich keine ZIP-Datei, sondern XML
            # Speichern Sie die XML-Datei direkt
            with open(path_definitions.MP_BASE_DATA, 'wb') as f:
                f.write(response.content)
            
            print("✓ MDBS gespeichert unter:", path_definitions.MP_BASE_DATA)

    except Exception as e:
        print(f"✗ Fehler: {str(e)}")