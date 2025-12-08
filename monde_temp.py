from netCDF4 import *
import numpy as np

nc = Dataset("DCENT_ensemble_1850_2023_ensemble_mean.nc", "r")

print(nc.variables['temperature'])

def couleur_monde(min_x , min_y , max_x, max_y):
    """
    Cette fonction doit retourne des carre de couleurs transparent sur la fenetre
    par dessus de la carte du monde
    """
    None