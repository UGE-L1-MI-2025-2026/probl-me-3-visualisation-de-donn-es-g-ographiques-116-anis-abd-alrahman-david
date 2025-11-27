from fltk import *
import shapefile

sf = shapefile.Reader("departements-20180101")
reco = sf.records()
outremer = ['974', '972', '971', '973', '976','2A','2B']


def bbox_france():
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

"""
se = sf.shape(29)
point_total = se.points
bbox = se.bbox
coo = []
for i in range (len(point_total)):
    point = se.points[i]
    x = (point[0] - bbox[0]) / (bbox[2] - bbox[0]) * 600
    y = (bbox[3] - point[1]) / (bbox[3] - bbox[1]) * 600
    coo.append([x,y])

print(se.parts)
"""

min_x , min_y , max_x, max_y = bbox_france()


cree_fenetre(600,600)

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
                x = (point[0] - min_x) / (max_x - min_x) * 600
                y = (max_y - point[1]) / (max_y - min_y) * 600
                coo.append([x,y])
            polygone(coo,couleur="white")
    else:
        continue

attend_ev()
ferme_fenetre()



"""
x = (longitude - longitude_min) / (longitude_max - longitude_min) * largeur_image
y = (latitude_max - latitude) / (latitude_max - latitude_min) * hauteur_image

['974', '972', '971', '973', '976']
"""