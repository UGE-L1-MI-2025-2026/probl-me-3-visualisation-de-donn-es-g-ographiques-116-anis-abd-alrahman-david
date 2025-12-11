from temperature import *
from afficher_carte import *
from fltk import *


LONGUEUR = 600

def animation(date,nom='france'):
    min_x , min_y , max_x, max_y = bbox_x(nom)
    min_jour = 1
    max_jour = 31
    jour = int(date[-2:])
    mois = date[5:7]
    annee = date[0:4]
    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        if tev == 'Touche':
            nom_touche = touche(ev)
            if nom_touche == 'Left':
                jour = jour - 1
                if jour < min_jour:
                    jour = max_jour
                
                date = f'2018-07-{jour:02d}'
                dico_temp,maxi,mini = temperature(date)
                efface_tout()
                palette_temp(LONGUEUR+100,650,maxi,mini)
                carte(nom,LONGUEUR,dico_temp,maxi,mini,min_x , min_y , max_x, max_y,date=date)

            elif nom_touche == 'Right':
                jour = jour + 1
                if jour > max_jour:
                    jour = min_jour
                date = f'2018-07-{jour:02d}'
                dico_temp,maxi,mini = temperature(date)
                efface_tout()
                palette_temp(LONGUEUR+100,650,maxi,mini)
                carte(nom,LONGUEUR,dico_temp,maxi,mini,min_x , min_y , max_x, max_y,date=date)
        elif tev == 'Quitte':
            break
        else:
            pass

        mise_a_jour()
                
