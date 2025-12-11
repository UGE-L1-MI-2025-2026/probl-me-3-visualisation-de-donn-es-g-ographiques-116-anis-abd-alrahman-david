# PARTIE ORIGINALE D'ABD + MODIFICATIONS PAR DAVID

from temperature import *
from afficher_carte import *
from fltk import *
from temperature import couleur as couleur_temperature  # CORRECTION: Import explicite

LONGUEUR = 600

# Variables pour le zoom et le déplacement (SANS global)
def animation(date, nom='france'):
    """
    Animation interactive avec gestion des touches.
    
    MODIFICATIONS PAR DAVID:
    - Ajout zoom/dézoom (flèches haut/bas)
    - Ajout déplacement (Q Z S D)
    - Ajout changement de date (flèches gauche/droite)
    - Ajout affichage info survol souris
    """
    # MODIFICATION: Variables locales au lieu de global
    zoom_level = 1.0
    offset_x = 0
    offset_y = 0
    deplacement_step = 20
    
    min_x, min_y, max_x, max_y = bbox_x(nom)
    
    # Extraire jour, mois, année de la date
    annee = int(date[0:4])
    mois = int(date[5:7])
    jour = int(date[8:10])
    
    # Limites des jours selon le mois
    jours_par_mois = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    
    # Gérer les années bissextiles
    if annee % 4 == 0 and (annee % 100 != 0 or annee % 400 == 0):
        jours_par_mois[2] = 29
    
    # Charger les températures initiales
    dico_temp, maxi, mini = temperature(date)
    
    # Dessiner la carte initiale et récupérer dept_info
    dept_info = carte_avec_transformation(nom, LONGUEUR, dico_temp, maxi, mini,
                                         min_x, min_y, max_x, max_y, date,
                                         zoom_level, offset_x, offset_y)
    
    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        
        if tev == 'Touche':
            nom_touche = touche(ev)
            redessiner = False
            
            # ========== NAVIGATION TEMPORELLE ==========
            if nom_touche == 'Left':
                jour -= 1
                if jour < 1:
                    mois -= 1
                    if mois < 1:
                        mois = 12
                        annee -= 1
                    jour = jours_par_mois[mois]
                redessiner = True
            
            elif nom_touche == 'Right':
                jour += 1
                if jour > jours_par_mois[mois]:
                    jour = 1
                    mois += 1
                    if mois > 12:
                        mois = 1
                        annee += 1
                redessiner = True
            
            # ========== ZOOM ==========
            elif nom_touche == 'Up':
                zoom_level *= 1.2
                if zoom_level > 5.0:
                    zoom_level = 5.0
                redessiner = True
            
            elif nom_touche == 'Down':
                zoom_level /= 1.2
                if zoom_level < 0.5:
                    zoom_level = 0.5
                redessiner = True
            
            # ========== DÉPLACEMENT ==========
            elif nom_touche == 'q' or nom_touche == 'Q':
                offset_x -= deplacement_step
                redessiner = True
            
            elif nom_touche == 'd' or nom_touche == 'D':
                offset_x += deplacement_step
                redessiner = True
            
            elif nom_touche == 'z' or nom_touche == 'Z':
                offset_y -= deplacement_step
                redessiner = True
            
            elif nom_touche == 's' or nom_touche == 'S':
                offset_y += deplacement_step
                redessiner = True
            
            # Redessiner si nécessaire
            if redessiner:
                date = f'{annee:04d}-{mois:02d}-{jour:02d}'
                dico_temp, maxi, mini = temperature(date)
                
                efface_tout()
                palette_temp(LONGUEUR + 100, 650, maxi, mini)
                
                # CORRECTION: Récupérer le nouveau dept_info
                dept_info = carte_avec_transformation(nom, LONGUEUR, dico_temp, maxi, mini,
                                                     min_x, min_y, max_x, max_y, date,
                                                     zoom_level, offset_x, offset_y)
        
        elif tev == 'Quitte':
            break
        
        # Afficher les infos de survol avec le dept_info actuel
        afficher_info_survol(dept_info)
        
        mise_a_jour()


def carte_avec_transformation(nom, longeur, dico_temp, maxi, mini, 
                              min_x, min_y, max_x, max_y, date,
                              zoom, offset_x, offset_y):
    """
    Dessine la carte avec application du zoom et du déplacement.
    
    Retourne: dict {id_polygone: (code_dept, tmoy)}
    """
    dept_info = {}
    
    if nom == 'france':
        texte(200, 710, "Température quotidienne des départements français", 
              taille=14, tag="titre")
        annee = date[:4]
        texte(540, 710, f"Année: {annee}", taille=14, tag="date")
    
    sf, reco = fichier(nom)
    
    for i in range(len(reco)):
        dep = sf.shape(i)
        code_dept = reco[i][0]
        parts = dep.parts
        parts_complet = list(parts) + [len(dep.points)]
        
        # ========== OUTRE-MER (sans zoom/déplacement) ==========
        if code_dept in outremer:
            points = dep.points
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            
            dept_min_x = min(xs)
            dept_max_x = max(xs)
            dept_min_y = min(ys)
            dept_max_y = max(ys)
            dept_width = dept_max_x - dept_min_x
            dept_height = dept_max_y - dept_min_y
            
            echelle = 60 / max(dept_width, dept_height)
            pos_x, pos_y = outremer_positions[code_dept]
            
            for k in range(len(parts_complet) - 1):
                debut = parts_complet[k]
                fin = parts_complet[k + 1]
                coo = []
                
                for j in range(debut, fin):
                    point = points[j]
                    x = (point[0] - dept_min_x) * echelle + pos_x
                    y = pos_y + (dept_max_y - point[1]) * echelle
                    coo.append([x, y])
                
                if code_dept in dico_temp:
                    couleur_dept = couleur_temperature(code_dept, 'tmax', dico_temp, maxi, mini)
                    tmoy = dico_temp[code_dept]['tmoy']
                    id_poly = polygone(coo, couleur="black", remplissage=couleur_dept,
                                      epaisseur=0.5, tag=f"dept_{code_dept}")
                    dept_info[id_poly] = (code_dept, tmoy)
                else:
                    polygone(coo, couleur="black", remplissage="#cccccc", epaisseur=0.5)
        
        # ========== MÉTROPOLE (avec zoom/déplacement) ==========
        else:
            for k in range(len(parts_complet) - 1):
                debut = parts_complet[k]
                fin = parts_complet[k + 1]
                coo = []
                visible = False
                
                for j in range(debut, fin):
                    point = dep.points[j]
                    x = ((point[0] - min_x) / (max_x - min_x) * longeur) * zoom + offset_x
                    y = ((max_y - point[1]) / (max_y - min_y) * 600) * zoom + offset_y
                    
                    if 0 <= x <= longeur and 0 <= y <= 600:
                        visible = True
                    
                    coo.append([x, y])
                
                if visible:
                    if code_dept not in probleme:
                        code_final = code_dept
                    else:
                        code_final = '69'
                    
                    if code_final in dico_temp:
                        couleur_dept = couleur_temperature(code_final, 'tmax', dico_temp, maxi, mini)
                        tmoy = dico_temp[code_final]['tmoy']
                        id_poly = polygone(coo, couleur="black",
                                          remplissage=couleur_dept if nom == "france" else "",
                                          tag=f"dept_{code_final}")
                        dept_info[id_poly] = (code_final, tmoy)
                    else:
                        polygone(coo, couleur="black", remplissage="#cccccc")
    
    return dept_info