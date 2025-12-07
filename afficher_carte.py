
# PARTIE ABD

from fltk import *
import shapefile
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def fichier(nom_fichier):
    """Ouvre et retourne un fichier shapefile."""
    sf = shapefile.Reader("data/" + nom_fichier)
    reco = sf.records()
    return sf, reco


outremer = ['974', '972', '971', '973', '976']
probleme = ["69D", '69M']


def bbox_x(nom):
    """
    Calcule les coordonnées extrêmes de la carte (hors outre-mer).
    Retourne: (min_x, min_y, max_x, max_y)
    """
    sf, reco = fichier(nom)
    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')
    
    for i in range(len(reco)):
        dep = sf.shape(i)
        if reco[i][0] not in outremer:
            bbox = dep.bbox
            min_x = min(min_x, bbox[0])
            min_y = min(min_y, bbox[1])
            max_x = max(max_x, bbox[2])
            max_y = max(max_y, bbox[3])
    
    return min_x, min_y, max_x, max_y


# PARTIE AJOUTÉE PAR david (pour gérer CSV et JSON)

def palette_temp(longeur, hauteur_fenetre, date, type_fichier, nom_fichier):
    """
    Dessine la palette de couleurs sur le côté droit de la fenêtre.
    
    MODIFICATION: Ajout des paramètres type_fichier et nom_fichier
    pour supporter à la fois CSV et JSON
    
    Paramètres:
        longeur (int): Largeur de la fenêtre
        hauteur_fenetre (int): Hauteur de la fenêtre
        date (str): Date des données
        type_fichier (str): 'csv' ou 'json'
        nom_fichier (str): Chemin du fichier de données
    """
    # MODIFICATION: Branchement conditionnel selon le type de fichier
    if type_fichier == 'csv':
        from lecture_csv import temperature_csv
        dico_temp, maxi, mini = temperature_csv(date, nom_fichier)
    else:  # json
        from temperature import temperature
        dico_temp, maxi, mini = temperature(date)
    
    chaque_5 = 9
    cmap = plt.get_cmap('plasma')
    bande = 5
    n = hauteur_fenetre // bande
    
    for i in range(n):
        value = i / (n - 1) if n > 1 else 0
        rgba = cmap(value)
        hex_color = mcolors.to_hex(rgba)
        
        rectangle(longeur - 10, i * bande, longeur, (i + 1) * bande,
                 remplissage=hex_color, couleur=hex_color)
        
        chaque_5 += 1
        if chaque_5 == 10:
            temp_reel = value * (maxi - mini) + mini
            texte(longeur - 40, i * bande, f"{int(temp_reel)}°-", taille=16)
            chaque_5 = 0


def obtenir_couleur_departement(code_dept, type_temp, date, type_fichier, nom_fichier):
    """
    Obtient la couleur d'un département selon le type de fichier.
    
    NOUVELLE FONCTION: Permet de gérer à la fois CSV et JSON
    en appelant la bonne fonction de coloration
    
    Paramètres:
        code_dept (str): Code du département
        type_temp (str): Type de température ('tmin', 'tmax', 'tmoy')
        date (str): Date des données
        type_fichier (str): 'csv' ou 'json'
        nom_fichier (str): Chemin du fichier de données
    
    Retourne:
        str: Couleur hexadécimale
    """
    if type_fichier == 'csv':
        from lecture_csv import couleur_csv
        return couleur_csv(code_dept, type_temp, date, nom_fichier)
    else:  # json
        from temperature import couleur
        return couleur(code_dept, type_temp, date)


# PARTIE abd modifiée par david

def carte(nom, date, type_fichier, nom_fichier):
    """
    Affiche la carte de France avec les températures colorées.
    
    MODIFICATIONS apportées à la fonction originale:
    1. Ajout du paramètre type_fichier pour supporter CSV et JSON
    2. Ajout du paramètre nom_fichier pour passer le nom du fichier utilisateur
    3. Appel à palette_temp() avec les nouveaux paramètres
    4. Appel à obtenir_couleur_departement() au lieu de couleur() directement
    5. Ajout de l'affichage de la date en haut de la fenêtre
    
    Paramètres:
        nom (str): Nom du fichier shapefile (ex: 'france')
        date (str): Date des données
        type_fichier (str): 'csv' ou 'json'
        nom_fichier (str): Nom du fichier donné par l'utilisateur
    """
    min_x, min_y, max_x, max_y = bbox_x(nom)
    sf, reco = fichier(nom)
    
    if nom == "france":
        longeur = 600
    else:
        longeur = 1000
    
    cree_fenetre(longeur + 100, 600)
    
    # MODIFICATION: Ajout de type_fichier et nom_fichier
    palette_temp(longeur + 100, 600, date, type_fichier, nom_fichier)
    
    for i in range(len(reco)):
        if reco[i][0] not in outremer:
            dep = sf.shape(i)
            parts = dep.parts
            parts_complet = list(parts) + [len(dep.points)]
            
            for k in range(len(parts_complet) - 1):
                debut = parts_complet[k]
                fin = parts_complet[k + 1]
                coo = []
                
                for j in range(debut, fin):
                    point = dep.points[j]
                    x = (point[0] - min_x) / (max_x - min_x) * longeur
                    y = (max_y - point[1]) / (max_y - min_y) * 600
                    coo.append([x, y])
                
                # MODIFICATION: Gestion des cas spéciaux 69D/69M
                if reco[i][0] not in probleme:
                    code = reco[i][0]
                else:
                    code = '69'
                
                # MODIFICATION: Utilisation de obtenir_couleur_departement()
                # au lieu de couleur() pour supporter CSV et JSON
                couleur_dept = obtenir_couleur_departement(code, 'tmax', date, type_fichier, nom_fichier)
                polygone(coo, couleur="black", remplissage=couleur_dept)
    
    # MODIFICATION: Ajout de l'affichage de la date
    texte(10, 10, f"Date: {date}", couleur="black", taille=20)
    
    mise_a_jour()