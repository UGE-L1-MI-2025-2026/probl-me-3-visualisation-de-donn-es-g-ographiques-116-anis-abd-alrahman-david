from fltk import *
from afficher_carte import *
from temperature import *
from animation import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def main(nom,date):
    dico_temp,maxi,mini = temperature(date)
    if nom == "france":
        longeur = 600 
    else:
        longeur = 1000
    cree_fenetre(longeur+100,600)
    palette_temp(longeur+100,600,maxi,mini)
    carte(nom,longeur,dico_temp,maxi,mini)
    attend_ev()
    ferme_fenetre()




main('france','2018-12-12')