from temperature import *
from afficher_carte import *
from fltk import *





def animation(date):
    min = 1
    max = 31
    jour = date[-2:]
    mois = date[5:7]
    annee = date[0:4]
    while True:
        ev = donne_ev
        tev = type_ev
        if tev == 'Touche':
            nom_touche = touche(ev)
            if nom_touche == 'Left':
                print('yes')
                jour = date[-2]
                int_jour = int(jour) - 1
                if int_jour < min:
                    int_jour = max
                    jour = str(int_jour)
                    date = '2018-07-{jour}'
                else:
                    jour = str(int_jour)
                    date = '2018-07-{jour}'
                temperature(date)
            elif nom_touche == 'Right':
                print('no')
                jour = date[-2]
                int_jour = int(jour) + 1
                if int_jour > max:
                    int_jour = min
                    jour = str(int_jour)
                    date = '2018-07-{jour}'
                else:
                    jour = str(int_jour)
                    date = '2018-07-{jour}'
                temperature(date)
        elif tev == 'Quitte':
            break
        else:
            pass

    mise_a_jour()
                