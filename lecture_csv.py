import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def lire_csv(nom_fichier):
    """
    Lit un fichier CSV et renvoie toutes les lignes sous forme de liste de listes.
    """
    with open(nom_fichier, 'r', encoding='utf-8-sig') as fichier:
        lignes = []
        for ligne in fichier:
            ligne = ligne.strip()
            if ligne:
                valeurs = ligne.split(';')
                lignes.append(valeurs)
        return lignes


def extraire_entete(lignes_csv):
    """Extrait l'entête (première ligne)."""
    return lignes_csv[0]


def extraire_donnees(lignes_csv):
    """Extrait les données (toutes les lignes sauf la première)."""
    return lignes_csv[1:]


def trouver_colonne(entete, nom_colonne):
    """Trouve l'index d'une colonne."""
    for i in range(len(entete)):
        if entete[i].strip() == nom_colonne:
            return i
    return -1


def charger_temperatures(nom_fichier):
    """
    Charge toutes les températures depuis le CSV.
    Retourne une liste de dictionnaires.
    
    Paramètres:
        nom_fichier (str): Nom du fichier CSV donné par l'utilisateur
    """
    try:
        lignes = lire_csv(nom_fichier)
    except FileNotFoundError:
        print(f"Erreur: Le fichier {nom_fichier} n'a pas été trouvé.")
        return []
        
    entete = extraire_entete(lignes)
    donnees = extraire_donnees(lignes)

    # Trouver les positions des colonnes
    pos_date = trouver_colonne(entete, 'Date')
    pos_code = trouver_colonne(entete, 'Code INSEE département')
    pos_nom = trouver_colonne(entete, 'Département')
    pos_tmin = trouver_colonne(entete, 'TMin (°C)')
    pos_tmax = trouver_colonne(entete, 'TMax (°C)')
    pos_tmoy = trouver_colonne(entete, 'TMoy (°C)')

    resultats = []
    for ligne in donnees:
        if len(ligne) > max(pos_date, pos_code, pos_nom, pos_tmin, pos_tmax, pos_tmoy):
            try:
                tmin = ligne[pos_tmin].strip()
                tmax = ligne[pos_tmax].strip()
                tmoy = ligne[pos_tmoy].strip()

                if tmin and tmax and tmoy:
                    dept = {
                        'date': ligne[pos_date].strip(),
                        'code': ligne[pos_code].strip(),
                        'nom': ligne[pos_nom].strip(),
                        'tmin': float(tmin.replace(',', '.')),
                        'tmax': float(tmax.replace(',', '.')),
                        'tmoy': float(tmoy.replace(',', '.'))
                    }
                    resultats.append(dept)
            except (ValueError, IndexError):
                continue

    return resultats


def obtenir_dates(nom_fichier):
    """
    Retourne toutes les dates uniques du CSV triées.
    
    Paramètres:
        nom_fichier (str): Nom du fichier CSV donné par l'utilisateur
    """
    donnees = charger_temperatures(nom_fichier)
    dates = []
    for entree in donnees:
        if 'date' in entree and entree['date'] not in dates:
            dates.append(entree['date'])
    return sorted(dates)


def obtenir_temp_et_limites_par_date(date_specifique, nom_fichier):
    """
    Charge les températures pour une date spécifique depuis le CSV.
    ALTERNATIVE float('inf'): Utilise None et initialise avec la première valeur.
    
    Paramètres:
        date_specifique (str): date au format du CSV (ex: '2018-01-01')
        nom_fichier (str): Nom du fichier CSV donné par l'utilisateur
        
    Retourne:
        tuple: (dict_temp_par_code, tmax_jour, tmin_jour)
    """
    departements = charger_temperatures(nom_fichier)
    if not departements:
        return {}, 0, 0

    dict_temp_par_code = {}
    tmin_jour = None  # Au lieu de float('inf')
    tmax_jour = None  # Au lieu de float('-inf')

    for dept in departements:
        if dept['date'] == date_specifique:
            dict_temp_par_code[dept['code']] = {
                'tmin': dept['tmin'],
                'tmax': dept['tmax'],
                'tmoy': dept['tmoy']
            }
            
            # Initialiser avec la première valeur trouvée
            if tmin_jour is None:
                tmin_jour = dept['tmin']
                tmax_jour = dept['tmax']
            else:
                tmin_jour = min(tmin_jour, dept['tmin'])
                tmax_jour = max(tmax_jour, dept['tmax'])

    # Gérer le cas où aucune donnée n'est trouvée
    if tmin_jour is None:
        tmin_jour = 0
    if tmax_jour is None:
        tmax_jour = 0

    return dict_temp_par_code, tmax_jour, tmin_jour


# ==================== PARTIE AJOUTÉE POUR COLORATION ====================
# Ces fonctions intègrent la logique de temperature.py pour le CSV

def calculer_couleur_departement(code_departement, type_temp, date, dico_temp, mini, maxi):
    """
    Calcule la couleur hexadécimale pour un département donné.
    Intègre la logique de coloration de temperature.py.
    
    Paramètres:
        code_departement (str): Code du département (ex: '75')
        type_temp (str): Type de température ('tmin', 'tmax', 'tmoy')
        date (str): Date au format CSV
        dico_temp (dict): Dictionnaire des températures par département
        mini (float): Température minimale du jour
        maxi (float): Température maximale du jour
    
    Retourne:
        str: Couleur au format hexadécimal (ex: '#ff5733')
    """
    if code_departement not in dico_temp:
        return '#cccccc'  # Gris par défaut si pas de données
    
    temp = dico_temp[code_departement][type_temp]
    
    if temp is None or maxi == mini:
        return '#cccccc'
    
    # Normaliser la température entre 0 et 1
    temp_normalisee = (temp - mini) / (maxi - mini)
    
    # Appliquer la palette plasma
    cmap = plt.get_cmap('plasma')
    couleur_rgba = cmap(temp_normalisee)
    hex_couleur = mcolors.to_hex(couleur_rgba)
    
    return str(hex_couleur)


def temperature_csv(date, nom_fichier):
    """
    Fonction équivalente à temperature() mais pour CSV.
    Retourne les données de température pour une date donnée.
    
    Paramètres:
        date (str): Date au format CSV (ex: '2018-01-01')
        nom_fichier (str): Nom du fichier CSV donné par l'utilisateur
    
    Retourne:
        tuple: (dico_temp, maxi, mini)
    """
    return obtenir_temp_et_limites_par_date(date, nom_fichier)


def couleur_csv(code_departement, type_temp, date, nom_fichier):
    """
    Fonction équivalente à couleur() mais pour CSV.
    Calcule la couleur hexadécimale pour un département donné.
    
    Paramètres:
        code_departement (str): Code du département
        type_temp (str): Type de température ('tmin', 'tmax', 'tmoy')
        date (str): Date au format CSV
        nom_fichier (str): Nom du fichier CSV donné par l'utilisateur
    
    Retourne:
        str: Couleur hexadécimale
    """
    dico_temp, maxi, mini = obtenir_temp_et_limites_par_date(date, nom_fichier)
    return calculer_couleur_departement(code_departement, type_temp, date, dico_temp, mini, maxi)