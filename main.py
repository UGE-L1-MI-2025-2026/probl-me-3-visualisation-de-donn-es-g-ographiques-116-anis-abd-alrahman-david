from fltk import *
from afficher_carte_final import *
from temperature_final import *
from animation_final import *
from monde_temp import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def main(nom, date='2018-07-01'):
    min_x, min_y, max_x, max_y = bbox_x(nom)
    dico_temp, maxi, mini = temperature(date)
    
    if nom == "france":
        longeur = 600
    else:
        longeur = 1000
    
    cree_fenetre(longeur + 150, 750)  # Élargir la fenêtre pour éviter le chevauchement avec la palette  # MODIFIÉ: 750 au lieu de 650
    
    # Dessiner la carte et récupérer dept_info
    dept_info = carte(nom, longeur, dico_temp, maxi, mini, 
                     min_x, min_y, max_x, max_y, date)
    
    # Fusionner titre et date
    titre_et_date = f"Carte des températures - {date}"
    texte((longeur + 100) // 2, 20, titre_et_date, ancrage='center', taille=14)
    palette_temp(longeur + 100, 700, maxi, mini)  # Élargir la hauteur pour éviter le chevauchement
    
    # Lancer l'animation
    animation(date, nom)
    
    ferme_fenetre()

if __name__ == "__main__":
    main('france')