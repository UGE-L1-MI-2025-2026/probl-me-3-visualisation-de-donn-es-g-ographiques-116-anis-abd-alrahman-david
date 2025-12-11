from netCDF4 import *
from fltk import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from afficher_carte import *

nc = Dataset("DCENT_ensemble_1850_2023_ensemble_mean.nc", "r")

longitude = nc.variables["lon"][:]
latidue = nc.variables["lat"][:]
time = nc.variables["time"][:]

def temperature_monde(longeur=1000,date=1584,annee=1998):
    """
    Cette fonction retourne un grillage de couleurs des temperature
    sur la carte du monde
    """
    #BBOX du quadrillage

    minx = min(longitude)
    miny = min(latidue)
    maxx = max(longitude)
    maxy = max(latidue)

    #Dessin du quadrillage
    largeur_pixel = longeur / len(longitude)
    hauteur_pixel = 600 / len(latidue)
    for i in range(len(longitude)):
        for k in range(len(latidue)):
            x = (longitude[i] - minx) / (maxx - minx) * longeur
            y = (maxy - latidue[k]) / (maxy - miny) * 600
            coo = [[x,y],
                   [x+largeur_pixel,y],
                   [x+largeur_pixel,y+hauteur_pixel],
                   [x,y+hauteur_pixel]]
            hexcouleur , maxi , mini = couleur_temp(k,i,date)
            polygone(coo,
                     couleur=hexcouleur if hexcouleur != "#000000" else "",
                     remplissage=hexcouleur if hexcouleur != "#000000" else "",
                     tag = "poly"
                     )
    palette_temp(longeur+100,650,maxi,mini)
    texte(525,610,f"{str(annee)}",tag="annee")


def couleur_temp(lat=0,lon=0,date=1584):
    maxi = np.nanmax(nc.variables['temperature'][date][:])
    mini = np.nanmin(nc.variables['temperature'][date][:])
    temp_normal = nc.variables['temperature'][date][lat][lon]
    temp_en_pourcent = (temp_normal - mini) / (maxi - mini)
    cmap = plt.get_cmap('plasma')
    couleur = cmap(temp_en_pourcent)
    hex_couleur = colors.to_hex(couleur)
    return str(hex_couleur) , maxi , mini

def animation_monde():
    date = 1584
    annee = 1998
    while True:
        ev = attend_ev()
        tev = type_ev(ev)
        if tev == "Quitte":
            break
        if tev == "Touche":
            cle = touche(ev)
            if cle == "Right":
                if annee >= 2014:
                    texte(580,610," - MAX",tag="max")
                else:
                    efface("min")
                    date += 12
                    annee += 1
                    efface("annee")
                    efface("poly")
                    temperature_monde(date=date,annee=annee)
            if cle == "Left":
                if annee <= 1982:
                    texte(580,610," - MIN",tag="min")
                else:
                    efface("max")
                    date -= 12
                    annee -= 1
                    efface("annee")
                    efface("poly")
                    temperature_monde(date=date,annee=annee)