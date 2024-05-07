#import networkx as nx
import json

#G = nx.Graph()

def charge_fichier(nom_fichier):
    """Creer une liste de films

    Args:
        nom_fichier (str): le chemin d'un fichier

    Returns:
        list: une liste de films
    """
    fichier_chargee = []
    fic = open(nom_fichier,'r')
    for ligne in fic:
        fichier_chargee.append(eval(ligne.strip()))
    fic.close()
    return fichier_chargee

les_films = charge_fichier("data.txt")

#A finir
def creer_json(un_fichier):
    json_file = open("data.json", "w")
    with open(un_fichier) as fic:
        for ligne in fic:
            ligne = eval(ligne+"\n")
            json.dump(ligne,json_file,sort_keys = False,ensure_ascii=False)

    json_file.close()

creer_json("data_test.txt")

def collabo(un_acteur,films):
    """Permet d'avoir les collaborateurs d'un acteur

    Args:
        acteur (str): un acteur
        films (list): une liste de film

    Returns:
        set: un ensemble d'acteurs
    """
    les_collabos = set()
    for film in films:
        for acteur in film["cast"]:
            if un_acteur == acteur:
                for acteur in film["cast"]:
                    if acteur != un_acteur:
                        les_collabos.add(acteur)
                break
    return les_collabos



def collabo_commmun(acteur1,acteur2,films):
    """Permet d'avoir les collaborateurs en commun de deux acteurs

    Args:
        acteur1 (str): _description_
        acteur2 (str): _description_
        films (_type_): _description_

    Returns:
        _type_: _description_
    """
    collabos_acteur1 = collabo(acteur1,films)
    collabos_acteur2 = collabo(acteur2,films)
    collabos_en_commun = set()
    for collabo_acteur1 in collabos_acteur1:
        for collabo_acteur2 in collabos_acteur2:
            if collabo_acteur2 == collabo_acteur1:
                collabos_en_commun.add(collabo_acteur1)
    return collabos_en_commun


def creer_liaison(film):
    res = []
    for acteur1 in film["cast"]:

        for acteur2 in film["cast"]:
            liaison = [acteur1]
            liaison.append(acteur2)
            res.append(liaison)
    return res

un_film = charge_fichier("data_test.txt")[0]
#print(creer_liaison(un_film))




# Q3

def collaborateurs_proches(G,u,k):
    """Fonction renvoyant l'ensemble des acteurs à distance au plus k de l'acteur u dans le graphe G. La fonction renvoie None si u est absent du graphe.
        
    Parametres:
        G: le graphe
        u: le sommet de départ
        k: la distance depuis u
    """
    if u not in G.nodes:
        print(u,"est un illustre inconnu")
        return None
    collaborateurs = set()
    collaborateurs.add(u)
    print(collaborateurs)
    for i in range(k):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    return collaborateurs


def est_proche(G,u,v,k=1):
    if v in collaborateurs_proches(G,u,k):
        return True
    else:
        return False
    
def distance_naive(G,u,v):
    k=1
    while (u not in collaborateurs_proches(G,v,k)):
        k+=1
    return k

def distance(G,u,v):
    ...