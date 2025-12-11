from fltk import *
from afficher_carte import *
from temperature import *
from animation import *
from monde_temp import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def main(nom,date='2018-07-01'):
    min_x , min_y , max_x, max_y = bbox_x(nom)
    dico_temp,maxi,mini = temperature(date)
    hexcouleur , maxii , minii = couleur_temp()
    if nom == "france":
        longeur = 600 
    else:
        longeur = 1000
    cree_fenetre(longeur+100,650)
    carte(nom,longeur,dico_temp,maxi,mini,min_x , min_y , max_x, max_y)
    if nom == "monde":
        temperature_monde(longeur)
        animation_monde()
    else:
        palette_temp(longeur+100,650,maxi,mini)
        animation(date)
    attend_ev()
    ferme_fenetre()




if __name__ == "__main__":
    main('france')