from fltk import *
import shapefile
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from temperature import *

def fichier(nom_fichier):
    sf = shapefile.Reader(nom_fichier)
    reco = sf.records()
    return sf , reco

outremer = ['974', '972', '971', '973', '976',"69D",'69M']

def bbox_x(nom):
    sf , reco = fichier(nom)
    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')
    for i in range(len(reco)):
        dep = sf.shape(i)
        if reco[i][0] not in outremer:
            bbox = dep.bbox
            min_x = min(min_x,bbox[0])
            min_y = min(min_y,bbox[1])
            max_x = max(max_x,bbox[2])
            max_y = max(max_y,bbox[3])
        else:
            continue
    return min_x , min_y , max_x, max_y

def palette_temp(longeur, hauteur_fenetre):
    cmap = plt.get_cmap('plasma')
    bande = 5 
    n = hauteur_fenetre // bande 
    for i in range(n):
        value = i / (n - 1)
        rgba = cmap(value)
        hex_color = mcolors.to_hex(rgba)
        
        rectangle(longeur - 10, i * bande, longeur, (i + 1) * bande,remplissage=hex_color, couleur=hex_color)
        y1 = 0
        if y1 == 5:
            texte(longeur - 35, i * bande, f"{value}°-", taille=10)
        y1 += 1




def carte(nom):
    min_x , min_y , max_x, max_y = bbox_x(nom)
    sf , reco = fichier(nom)
    if nom == "france":
        longeur = 600 
    else:
        longeur = 1000
    cree_fenetre(longeur+100,600)
    palette_temp(longeur+100,600)
    for i in range(len(reco)):
        if reco[i][0] not in outremer:
            dep = sf.shape(i)
            parts = dep.parts
            parts_complet = list(parts) + [len(dep.points)]
        
            for k in range(len(parts_complet)-1):
                debut = parts_complet[k]
                fin = parts_complet[k+1]
                coo = []

                for j in range(debut,fin):
                    point = dep.points[j]
                    x = (point[0] - min_x) / (max_x - min_x) * longeur
                    y = (max_y - point[1]) / (max_y - min_y) * 600
                    coo.append([x,y])
                polygone(coo,couleur="black",remplissage=couleur(reco[i][0],'tmax'))
        else:
            continue

    attend_ev()
    ferme_fenetre()

carte("france")