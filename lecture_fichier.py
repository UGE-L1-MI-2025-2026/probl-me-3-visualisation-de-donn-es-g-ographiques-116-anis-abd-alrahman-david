import csv 

def lire_csv(nom_fichier):
    """
    Lit un fichier csv ligne par ligne et Renvoie une liste de lignes (chaque ligne est une liste de valeurs)
    """
    with open(nom_fichier, 'r', encoding='utf-8') as fichier :
        lignes = []
        for ligne in fichier :
            ligne = ligne.strip() #on enleve les espace et retours a la ligne
            if ligne:   # si la ligne n'est pas vide
                valeurs = ligne.split(',')  # on découpe au niveau des virgules
                lignes.append(valeurs)
        return lignes

def extraire_entete(lignes_csv):
    """Extrait l'entête (la première ligne) d'un fichier CSV sous forme de liste de noms de colonnes."""
    return lignes_csv[0]

def extraire_donnees(lignes_csv):
    """Extrait les données (toutes les lignes sauf la première) d'un fichier CSV sous forme de liste de listes."""
    return lignes_csv[1:]

def trouver_position_colonne(entete, nom_colonne):
    """Trouve la position (index) d'une colonne donnée dans l'entête."""
    for i in range(len(entete)):
        if entete[i].strip() == nom_colonne:
            return i
    return -1  # Retourne -1 si la colonne n'est pas trouvée

def obtenir_stations_meteo():
    """Lit un fichier des stations météo et renvoie les informations importates 
    - return : liste de dictionnnaires, 1 par station météo
    chque dictionnaire contient les clés :  'nom', 'latitude', 'longitude', 'temperature'
    """
    lignes = lire_csv("data/stations_meteo.csv")
    entete = extraire_entete(lignes)
    donnees = extraire_donnees(lignes)

    pos_nom = trouver_position_colonne(entete, 'nom')
    pos_latitude = trouver_position_colonne(entete, 'latitude')
    pos_longitude = trouver_position_colonne(entete, 'longitude')
    pos_temperature = trouver_position_colonne(entete, 'temperature')

    stations = []
    for ligne in donnees :
        if len(ligne) > max(pos_nom, pos_latitude, pos_longitude, pos_temperature):
            station = {}
            station['nom'] = ligne[pos_nom].strip()
            station['latitude'] = float(ligne[pos_latitude].strip())
            station['longitude'] = float(ligne[pos_longitude].strip())
            station['temperature'] = float(ligne[pos_temperature].strip())
            stations.append(station)
    return stations

def filtrer_station_par_temperature(stations, temp_min, temp_max):
    """Filtre les stations météo dont la température est comprise entre temp_min et temp_max (inclus).
    - return : liste de dictionnaires des stations filtrées"""
    stations_filtrees = []
    for station in stations:
        if temp_min <= station['temperature'] <= temp_max:
            stations_filtrees.append(station)
    return stations_filtrees


if __name__ == "__main__":
    # Test 1 : Lire le fichier
    print("=== TEST 1 : Lecture du fichier ===")
    lignes = lire_csv("data/stations_meteo.csv")
    print(f"Nombre de lignes lues : {len(lignes)}")
    print(f"Première ligne : {lignes[0]}")

    # Test 2 : Extraire l'entête
    print("\n=== TEST 2 : Entête ===")
    entete = extraire_entete(lignes)
    print(f"Colonnes : {entete}")

    # Test 3 : Obtenir les stations
    print("\n=== TEST 3 : Stations ===")
    stations = obtenir_stations_meteo()
    print(f"Nombre de stations : {len(stations)}")
    if len(stations) > 0:
        print(f"Première station : {stations[0]}")