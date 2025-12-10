from netCDF4 import *
from fltk import *
import numpy as np

nc = Dataset("DCENT_ensemble_1850_2023_ensemble_mean.nc", "r")

longitude = nc.variables["lon"][:]
latidue = nc.variables["lat"][:]
time = nc.variables["time"][:]

def temperature_monde(longeur=1000):
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
            polygone(coo,couleur='black')


def couleur_temp():
    None


lon = longitude[0]
lat = latidue[0]
print("="*10,"Temperature","="*10)
print(nc.variables['temperature'][1584][0][0])


temps = nc.variables['time']


"""
Les indice de time c est menseulle donc chaque indice c est 1 mois
donc le 1er janvier 1982 correspond a l indice 1584
Pour passer d une annee a l autre il suffit d ajouter 12 a chaque indice
le temps pour la temperature doit etre entre 1982--2014
la variable time commence le 1er janvier 1850
les parametre de temperature sont 
temperature[time par mois][indice de la latitude][indice de la longitude]
"""