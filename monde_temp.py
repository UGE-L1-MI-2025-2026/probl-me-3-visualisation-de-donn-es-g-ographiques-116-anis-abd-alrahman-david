from netCDF4 import *

nc = Dataset("DCENT_ensemble_1850_2023_ensemble_mean.nc", "r")

print(nc.dimensions['lon'])

def couleur_monde():
    