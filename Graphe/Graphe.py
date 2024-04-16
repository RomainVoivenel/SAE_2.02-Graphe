import networkx as nx
import csv

G = nx.Graph()

def charge_fichier(nom_fichier):
    fichier_chargee = []
    fic = open(nom_fichier,'r')
    for ligne in fic:
        fichier_chargee.append(eval(ligne.strip()))
    fic.close()
    return fichier_chargee

def creer_liaison(film):
    res = []
    for acteur1 in film["cast"]:

        for acteur2 in film["cast"]:
            liaison = [acteur1]
            liaison.append(acteur2)
            res.append(liaison)
    return res

un_film = charge_fichier("data_test.txt")[0]
print(creer_liaison(un_film))