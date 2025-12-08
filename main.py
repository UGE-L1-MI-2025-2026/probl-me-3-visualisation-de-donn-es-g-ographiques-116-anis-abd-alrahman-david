from fltk import *
from afficher_carte import *
from temperature import *
from animation import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors

OUTREMER = ['974', '972', '971', '973', '976']
PROBLEME = ["69D", '69M']



def main():
    carte('france')
    animation()


