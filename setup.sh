#!/bin/bash

# Prüfe, ob Python 3.11 installiert ist
if ! command -v py -3.11 &> /dev/null
then
    echo "Python 3.11 ist nicht installiert."
    exit 1
fi

# Erstelle eine virtuelle Umgebung für Python 3.11
py -3.11 -m venv .venv

# Aktiviere die virtuelle Umgebung
source ./.venv/Scripts/activate


# Installiere pip-Abhängigkeiten
pip install --upgrade pip
pip install -r requirements.txt

# Optional: Installiere od_lib als Entwicklungsmodul
# cd src/
# pip install -e .
