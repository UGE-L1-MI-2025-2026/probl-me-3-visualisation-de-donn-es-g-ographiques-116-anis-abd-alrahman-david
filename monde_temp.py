from netCDF4 import Dataset

rootgrp = Dataset("DCENT_ensemble_1850_2023_ensemble_mean.nc", "w", format="NETCDF4")
print(rootgrp.data_model)