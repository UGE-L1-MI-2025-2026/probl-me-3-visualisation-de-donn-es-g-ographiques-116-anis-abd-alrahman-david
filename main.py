import shapefiles

sf = shapefile.Reader("routes.shp")

for shape, record in zip(sf.shapes(), sf.records()):
    print("Route : ", record[0])
    print("Coordonnées : ", shape.points[:5], "...")  # afficher les 5 premières
