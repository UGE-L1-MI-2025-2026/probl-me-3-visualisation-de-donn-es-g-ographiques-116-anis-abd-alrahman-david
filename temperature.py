from json import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def temperature(d):
    dico_temp = {}
    with open("temperature-quotidienne-departementale.json","r",encoding="utf-8") as f:
        data = load(f)
    mini = 40
    maxi= 0
    for depar in data:
        if depar['date_obs'] == f'2018-07-{d}':
            code_departement = depar['code_insee_departement']
            tmax = depar['tmax']
            tmin = depar['tmin']
            tmoy = depar['tmoy']  
            dico_temp[code_departement] = {'tmin' : tmin, 'tmax' : tmax, 'tmoy' : tmoy}
            if tmax is not None and tmax > maxi:
                maxi = tmax
            if  tmin is not None and tmin < mini:
                mini = tmin
    return dico_temp, maxi, mini
temperature('01')

def couleur(departement,tempera,d):
    dico_temp,maxi,mini = temperature(d)
    nom = dico_temp[departement]
    temp = nom[tempera]
    temp = (temp - mini) / (maxi - mini)
    cmap = plt.get_cmap('plasma')
    couleur = cmap(temp) 
    hex_couleur = colors.to_hex(couleur)
    return str(hex_couleur)