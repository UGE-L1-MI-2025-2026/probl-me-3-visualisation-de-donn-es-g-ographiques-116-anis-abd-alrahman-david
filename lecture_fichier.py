
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def lire_csv(nom_fichier):
    """
    Lit un fichier CSV et renvoie toutes les lignes sous forme de liste de listes.
    - nom_fichier : chemin vers le fichier CSV (str)
    - return : liste de listes, chaque sous-liste représente une ligne du fichier
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
    """
    Trouve l’index d’une colonne.
    """
    for i in range(len(entete)):
        if entete[i].strip() == nom_colonne:
            return i
    return -1


def charger_temperatures():
    """
    Charge toutes les températures depuis le CSV.
    Retourne une liste de dictionnaires :
    {
        'date': ... ,
        'code': ... ,
        'nom': ... ,
        'tmin': float,
        'tmax': float,
        'tmoy': float
    }
    """
    lignes = lire_csv("data/temperature-quotidienne-departementale.csv")
    entete = extraire_entete(lignes)
    donnees = extraire_donnees(lignes)

    # Trouver les positions
    pos_date = trouver_colonne(entete, 'Date')
    pos_code = trouver_colonne(entete, 'Code INSEE département')
    pos_nom = trouver_colonne(entete, 'Département')
    pos_tmin = trouver_colonne(entete, 'TMin (°C)')
    pos_tmax = trouver_colonne(entete, 'TMax (°C)')
    pos_tmoy = trouver_colonne(entete, 'TMoy (°C)')

    if -1 in [pos_date, pos_code, pos_nom, pos_tmin, pos_tmax, pos_tmoy]:
        raise ValueError("Une ou plusieurs colonnes sont introuvables dans le CSV.")

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
                        'tmin': float(tmin),
                        'tmax': float(tmax),
                        'tmoy': float(tmoy)
                    }
                    resultats.append(dept)
            except (ValueError, IndexError):
                continue

    return resultats



#  Fonction couleur 


def couleur_tmoy(tmoy, mini, maxi):
    """
    Renvoie une couleur hexadécimale selon la température tmoy,
    utilisant la palette 'plasma' de matplotlib (bleu → rouge).
    """
    # Normalisation
    t_norm = (tmoy - mini) / (maxi - mini)
    t_norm = max(0, min(1, t_norm))  # clamp 0..1

    cmap = plt.get_cmap('plasma')
    couleur = cmap(t_norm)
    return colors.to_hex(couleur)


def obtenir_dates():
    """Retourne toutes les dates uniques."""
    donnees = charger_temperatures()
    dates = []
    for entree in donnees:
        if 'date' in entree:
            if entree['date'] not in dates:
                dates.append(entree['date'])
    return dates


def filtrer_par_temperature(departements, temp_min, temp_max):
    """
    Filtre les départements dont tmoy est entre temp_min et temp_max.
    """
    departements_filtres = []
    for dept in departements:
        if temp_min <= dept['tmoy'] <= temp_max:
            departements_filtres.append(dept)
    return departements_filtres


def obtenir_temp_par_date(date_specifique=None):
    """
    Retourne un dict {code_departement : tmoy}
    """
    departements = charger_temperatures()
    if not departements:
        return {}

    if date_specifique is None:
        date_specifique = departements[0]['date']

    temp_par_dep = {}
    for dept in departements:
        if dept['date'] == date_specifique:
            temp_par_dep[dept['code']] = dept['tmoy']

    return temp_par_dep



# Exemple d’ajout automatique de la couleur


def ajouter_couleurs(donnees):
    """
    Ajoute une clé 'couleur' à chaque entrée de données.
    """
    mini = min(d['tmoy'] for d in donnees)
    maxi = max(d['tmoy'] for d in donnees)

    for dept in donnees:
        dept['couleur'] = couleur_tmoy(dept['tmoy'], mini, maxi)

    return donnees



#  Tests


if __name__ == "__main__":
    print("=== TEST Chargement ===")
    donnees = charger_temperatures()
    print(f"Entrées : {len(donnees)}")

    print("=== Ajout des couleurs ===")
    donnees_colorees = ajouter_couleurs(donnees)
    print(donnees_colorees[0])

    print("=== TEST 1 : Lecture ===")
    lignes = lire_csv("data/temperature-quotidienne-departementale.csv")
    print(f"Lignes lues : {len(lignes)}")
    
    print("\n=== TEST 2 : Entête ===")
    entete = extraire_entete(lignes)
    print(f"Colonnes : {entete[:3]}...")
    
    print("\n=== TEST 4 : Par date ===")
    temp = obtenir_temp_par_date()
    print(f"Départements : {len(temp)}")
    
    print("\n=== TEST 5 : Filtrage ===")
    filtres = filtrer_par_temperature(donnees, 15, 20)
    print(f"Entre 15-20°C : {len(filtres)}")
