from fltk import *
from afficher_carte_final import *
from temperature_final import *
from animation_final import *
from monde_temp import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def main(nom, date='2018-07-01'):
    min_x, min_y, max_x, max_y = bbox_x(nom)
    
    if nom == "france":
        longeur = 600
    else:
        longeur = 1000
    
    # Créer la fenêtre avec sa taille d'origine
    cree_fenetre(longeur + 100, 750)
    
    # Lancer directement l'animation qui s'occupe de tout dessiner
    animation(date, nom)
    
    ferme_fenetre()

if __name__ == "__main__":
    main('france')