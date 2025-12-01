from json import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def temperature():
    dico_temp = {}
    with open("temperature-quotidienne-departementale.json","r",encoding="utf-8") as f:
        data = load(f)

    for depar in data:
        nom_departement = depar['departement']
        tmax = depar['tmax'] 
        tmin = depar['tmin']
        tmoy = depar['tmoy']    
        dico_temp[nom_departement] = {'tmin' : tmin, 'tmax' : tmax, 'tmoy' : tmoy}
    return dico_temp
print(temperature())

dico_temp = temperature()
def couleur(departement,tempera):
    nom = dico_temp[departement]

    temp = nom[tempera]

    temp_min,temp_max = 0 , 40

    temp = (temp - temp_min) / (temp_max - temp_min)
    cmap = plt.get_cmap('plasma')


    couleur = cmap(temp) 

    hex_couleur = colors.to_hex(couleur)
    return str(hex_couleur)



    
    