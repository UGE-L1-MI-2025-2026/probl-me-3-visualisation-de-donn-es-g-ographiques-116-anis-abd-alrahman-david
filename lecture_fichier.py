import csv 

def lire_csv(nom_fichier):
    """
    Lit un fichier csv ligne par ligne et Renvoie une liste de lignes (chaque ligne est une liste de valeurs)
    """
    
    with open(nom_fichier, 'r', encoding='utf-8') as fichier :
        lignes = []
        for ligne in fichier :
            ligne = ligne.strip #on enleve les espace et retours a la ligne
            if ligne:   # si la ligne n'est pas vide
                valeurs = ligne.split(',')  # on découpe au niveau des virgules
                lignes.append(valeurs)
        return lignes

def extraire_entete(lignes_csv):
    return lignes_csv[0]

def extraire_donnees(lignes_csv):
    return lignes_csv[1:]

def trouver_position_colonne(entete, nom_colonne):
    