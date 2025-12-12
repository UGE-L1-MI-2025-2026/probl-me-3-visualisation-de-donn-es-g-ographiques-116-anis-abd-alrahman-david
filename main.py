from fltk import *
from afficher_carte import *
from temperature import *
from animation import *
from monde_temp import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def main(nom, date='2018-12-31'):
    min_x, min_y, max_x, max_y = bbox_x(nom)
    hexcouleur , maxii , minii = couleur_temp()
    dico_temp, maxi, mini = temperature(date)
    
    if nom == "france":
        longeur = 600
        largeur = 750
    else:
        longeur = 1000
        largeur = 650
     
    cree_fenetre(longeur+100,largeur)
    if nom == "monde":
        carte(nom,longeur,dico_temp,maxi,mini,min_x , min_y , max_x, max_y)
        temperature_monde(longeur)
        animation_monde()
    else:
        palette_temp(longeur + 100, 700, maxi, mini)
        animation(date,nom)
        titre_et_date = f"Carte des températures - {date}"
        texte((longeur + 100) // 2, 20, titre_et_date, ancrage='center', taille=14)

    attend_ev()
    ferme_fenetre()


    
    ferme_fenetre()

if __name__ == "__main__":
    main('france')