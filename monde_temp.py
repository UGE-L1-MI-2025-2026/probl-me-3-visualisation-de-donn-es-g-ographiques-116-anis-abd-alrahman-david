from netCDF4 import *
from fltk import *

nc = Dataset("DCENT_ensemble_1850_2023_ensemble_mean.nc", "r")

"""
print("="*10,"Longitude","="*10)
longitude = nc.variables["lon"][:]
print("="*10,"Latitude","="*10)
latidue = nc.variables["lat"][:]
print("="*10,"Time","="*10)
print(nc.variables["time"][:])
print("="*10,"Info","="*10)
print(nc)
"""

def couleur_monde(min_x , min_y , max_x, max_y,longeur):
    """
    Cette fonction doit retourne des carre de couleurs transparent sur la fenetre
    par dessus de la carte du monde
    """
    longitude = nc.variables["lon"][:]
    latidue = nc.variables["lat"][:]
    coo = []
    for i in range(len(longitude)):
        for k in range(len(latidue)):
            x = (longitude[i] - min_x) / (max_x - min_x) * longeur
            y = (max_y - latidue[k]) / (max_y - min_y) * 600
            coo.append([x,y])
        polygone(coo,couleur='black')
    None