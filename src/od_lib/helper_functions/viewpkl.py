import pickle
import pandas as pd

# Pfad zur .pkl-Datei -> anpassen!
file_path = '/data/02_cached/factions/stage_01/factions.pkl'

# Datei laden
with open(file_path, 'rb') as file:
    data = pickle.load(file)

# Zeige den Inhalt an (z.B. das erste Element oder eine Zusammenfassung)
print(data)
