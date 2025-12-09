from netCDF4 import *
from fltk import *
import numpy as np

nc = Dataset("DCENT_ensemble_1850_2023_ensemble_mean.nc", "r")



longitude = nc.variables["lon"][:]
latidue = nc.variables["lat"][:]
time = nc.variables["time"][:]

"""
print("="*10,"Longitude","="*10)
print(longitude[0])
print("="*10,"Latitude","="*10)
print(latidue[0])
print("="*10,"Time","="*10)
print(time[20])
print("="*10,"Temperature","="*10)
#TRavile sur la tempeature on doit change ca shape
print(nc.variables['temperature'].shape)
"""
def couleur_monde(longeur=1000):
    """
    Cette fonction doit retourne des carre de couleurs transparent sur la fenetre
    par dessus de la carte du monde
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