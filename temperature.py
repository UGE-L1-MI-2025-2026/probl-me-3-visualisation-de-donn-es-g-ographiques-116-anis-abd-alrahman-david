from json import *

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