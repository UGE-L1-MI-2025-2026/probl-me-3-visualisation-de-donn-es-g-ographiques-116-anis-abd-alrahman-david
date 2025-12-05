from temperature import *
from afficher_carte import *
from fltk import *

def animation():
    while True:
        ev = donne_ev
        tev = type_ev
        if tev == 'Touche':
            nom_touche = touche(ev)
            if nom_touche == 'Left':
                da = int(d) - 1
                d = str(da)
                temperature(d)
                carte('france',d)
            elif nom_touche == 'Right':
                da = int(d) + 1
                d = str(da)
                temperature(d)
                carte('france',d)
            