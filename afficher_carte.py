from fltk import *
import shapefile
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from temperature import couleur as couleur_temperature  # CORRECTION: Renommer pour éviter conflit avec fltk

def fichier(nom_fichier):
    """Ouvre et lit un fichier shapefile."""
    sf = shapefile.Reader("data/"+nom_fichier)
    reco = sf.records()
    return sf, reco

# Liste des codes départements d'outre-mer
outremer = ['974', '972', '971', '973', '976']
probleme = ["69D", '69M']

# Positions alignées verticalement à gauche
outremer_positions = {
    '971': (20, 360),   # Guadeloupe
    '972': (20, 430),   # Martinique
    '973': (20, 500),   # Guyane
    '974': (20, 570),   # Réunion
    '976': (20, 640)    # Mayotte (augmenté pour fenêtre plus haute)
}

def bbox_x(nom):
    """
    Calcule les coordonnées extrêmes de la carte métropolitaine (sans outre-mer).
    
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


def palette_temp(longeur, hauteur_fenetre, maxi, mini):
    """Dessine la palette de couleurs sur le côté droit de la fenêtre."""
    efface("pal")
    chaque_5 = 9
    cmap = plt.get_cmap('plasma')
    bande = 5
    n = hauteur_fenetre // bande
    
    for i in range(n):
        value = i / (n - 1)
        rgba = cmap(value)
        hex_color = mcolors.to_hex(rgba)
        
        rectangle(longeur - 10, i * bande, longeur, (i + 1) * bande,
                 remplissage=hex_color, couleur=hex_color, tag='pal')
        
        chaque_5 += 1
        if chaque_5 == 10:
            temp_reel = value * (maxi - mini) + mini
            texte(longeur - 40, i * bande, f"{int(temp_reel)}°-", taille=16, tag='pal')
            chaque_5 = 0


def carte(nom, longeur, dico_temp, maxi, mini, min_x, min_y, max_x, max_y, date="2018-07-01"):
    """
    Dessine la carte de France avec :
    - La métropole au centre
    - Les départements d'outre-mer alignés à gauche
    
    Retourne: Dictionnaire {id_polygone: (code_dept, tmoy)} pour le survol
    """
    dept_info = {}  # MODIFICATION: Retourner au lieu d'utiliser global
    
    if nom == 'france':
        # Afficher le titre centré en bas
        texte(200, 710, "Température quotidienne des départements français", 
              taille=14, tag="titre")
        
        # Afficher la date à côté du titre
        annee = date[:4]
        texte(540, 710, f"Année: {annee}", taille=14, tag="date")
    
    sf, reco = fichier(nom)
    
    for i in range(len(reco)):
        dep = sf.shape(i)
        code_dept = reco[i][0]
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
                
                if code_dept not in probleme:
                    code_final = code_dept
                else:
                    code_final = '69'
                
                if code_final in dico_temp:
                    couleur_dept = couleur_temperature(code_final, 'tmoy', dico_temp, maxi, mini)
                    tmoy = dico_temp[code_final]['tmoy']
                    id_poly = polygone(coo, couleur="black",
                                      remplissage=couleur_dept if nom == "france" else "",
                                      tag=f"dept_{code_final}")
                    dept_info[id_poly] = (code_final, tmoy)
                else:
                    polygone(coo, couleur="black", remplissage="#cccccc")
    
    return dept_info  # MODIFICATION: Retourner le dictionnaire


def afficher_info_survol(dept_info):
    """
    Affiche les infos du département survolé.
    
    Paramètres:
        dept_info (dict): Dictionnaire {id_polygone: (code_dept, tmoy)}
    """
    survoles = liste_objets_survoles()
    
    efface("info_survol")
    
    for obj_id in survoles:
        if obj_id in dept_info:
            code, tmoy = dept_info[obj_id]
            # MODIFICATION: Afficher en haut à gauche avec fond blanc
            rectangle(5, 5, 250, 35, remplissage="white", couleur="black", tag="info_survol")
            texte(10, 10, f"Département {code} | tmoy : {tmoy:.1f}°C",
                 couleur="black", taille=12, tag="info_survol")
            break