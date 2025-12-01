import csv 

def lire_csv(nom_fichier):
    """
    Lit un fichier csv ligne par ligne et Renvoie une liste de lignes (chaque ligne est une liste de valeurs)
    """
    with open(nom_fichier, 'r', encoding='utf-8-sig') as fichier:  # utf-8-sig enlève le BOM
        lignes = []
        for ligne in fichier:
            ligne = ligne.strip()
            if ligne:
                valeurs = ligne.split(';')
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
    return -1

def obtenir_stations_meteo():
    """
    Lit un fichier des stations météo et renvoie les informations importantes 
    - return : liste de dictionnaires, 1 par station météo
    chaque dictionnaire contient les clés : 'nom', 'latitude', 'longitude', 'temperature'
    
    ATTENTION : Ce fichier CSV contient des données par département, pas par station.
    Les colonnes sont : Date, Code INSEE département, Département, TMin, TMax, TMoy
    """
    lignes = lire_csv("data/temperature-quotidienne-departementale.csv")
    entete = extraire_entete(lignes)
    donnees = extraire_donnees(lignes)

    print("Entête du fichier :", entete)
    
    pos_date = trouver_position_colonne(entete, 'Date')
    pos_code = trouver_position_colonne(entete, 'Code INSEE département')
    pos_nom = trouver_position_colonne(entete, 'Département')
    pos_tmin = trouver_position_colonne(entete, 'TMin (°C)')
    pos_tmax = trouver_position_colonne(entete, 'TMax (°C)')
    pos_tmoy = trouver_position_colonne(entete, 'TMoy (°C)')
    
    print(f"Positions trouvées - Date:{pos_date}, Code:{pos_code}, Nom:{pos_nom}, TMin:{pos_tmin}, TMax:{pos_tmax}, TMoy:{pos_tmoy}")

    departements = []
    for ligne in donnees:
        if len(ligne) > max(pos_nom, pos_tmin, pos_tmax, pos_tmoy):
            try:
                tmin_str = ligne[pos_tmin].strip()
                tmax_str = ligne[pos_tmax].strip()
                tmoy_str = ligne[pos_tmoy].strip()
                
                if tmin_str and tmax_str and tmoy_str:
                    departement = {
                        'date': ligne[pos_date].strip() if pos_date >= 0 else '',
                        'code': ligne[pos_code].strip() if pos_code >= 0 else '',
                        'nom': ligne[pos_nom].strip(),
                        'tmin': float(tmin_str),
                        'tmax': float(tmax_str),
                        'tmoy': float(tmoy_str)
                    }
                    departements.append(departement)
            except (ValueError, IndexError):
                continue
    
    return departements

def filtrer_par_temperature(departements, temp_min, temp_max):
    """
    Filtre les départements dont la température moyenne est comprise entre temp_min et temp_max (inclus).
    Retourne une liste de dictionnaires des départements filtrés.
    """
    departements_filtres = []
    for dept in departements:
        if temp_min <= dept['tmoy'] <= temp_max:
            departements_filtres.append(dept)
    return departements_filtres

def obtenir_temperatures_departements(date_specifique=None):
    """
    Retourne un dictionnaire {code_departement: temperature_moyenne}
    Si date_specifique est fournie, filtre sur cette date.
    Sinon prend la première date disponible.
    """
    departements = obtenir_stations_meteo()
    
    if not departements:
        return {}
    
    if date_specifique is None:
        date_specifique = departements[0]['date']
        print(f"Aucune date spécifiée, utilisation de : {date_specifique}")
    
    temp_par_dep = {}
    for dept in departements:
        if dept['date'] == date_specifique:
            temp_par_dep[dept['code']] = dept['tmoy']
    
    return temp_par_dep


if __name__ == "__main__":
    print("=== TEST 1 : Lecture du fichier ===")
    lignes = lire_csv("data/temperature-quotidienne-departementale.csv")
    print(f"Nombre de lignes lues : {len(lignes)}")
    print(f"Première ligne : {lignes[0]}")
    
    print("\n=== TEST 2 : Entête ===")
    entete = extraire_entete(lignes)
    print(f"Colonnes : {entete}")

    print("\n=== TEST 3 : Départements ===")
    departements = obtenir_stations_meteo()
    print(f"Nombre d'entrées : {len(departements)}")
    if len(departements) > 0:
        print(f"Première entrée : {departements[0]}")
        print(f"Dernière entrée : {departements[-1]}")
    
    print("\n=== TEST 4 : Températures par département ===")
    temp_dep = obtenir_temperatures_departements()
    print(f"Nombre de départements : {len(temp_dep)}")
    if temp_dep:
        for code, temp in list(temp_dep.items())[:5]:
            print(f"  Département {code}: {temp}°C")
    
    print("\n=== TEST 5 : Filtrage ===")
    filtres = filtrer_par_temperature(departements, 15, 20)
    print(f"Départements avec température entre 15 et 20°C : {len(filtres)}")
    if filtres:
        print(f"Exemple : {filtres[0]}")
