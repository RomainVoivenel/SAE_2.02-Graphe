import networkx as nx
import matplotlib.pyplot as plt
import json

#G = nx.Graph()

def charge_fichier(nom_fichier:str):
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

def creer_json(un_fichier:str):
    """Permet de convertir un fichier txt en json

    Args:
        un_fichier (str): un fichier txt
    """
    txt_file = charge_fichier(un_fichier)
    json_file = open("data.json", "w")
    with open(un_fichier) as fic:
        json.dump(txt_file,json_file,sort_keys=False,ensure_ascii=False)
    json_file.close()

def tout_les_acteurs(un_fichier:str):
    """Permet d'avoir l'ensemble des acteurs dans un fichier json

    Args:
        un_fichier (str): un fichier json

    Returns:
        set: l'ensemble des acteurs
    """
    res = set()
    json_file = charge_fichier(un_fichier)
    for films in json_file[0]:
        for acteur in films["cast"]:
            res.add(acteur)
    return res

def json_vers_nx(un_fichier:str):
    graph = nx.Graph()
    liste_films = charge_fichier(un_fichier)[0]
    for i in range(len(liste_films)):
        for acteur in liste_films[i]["cast"]:
            if acteur not in graph.nodes():
                graph.add_node(acteur)
            for autre_acteur in liste_films[i]["cast"]:
                if acteur != autre_acteur and (acteur,autre_acteur) not in graph.edges():
                    graph.add_edge(acteur,autre_acteur)
    return graph


G = json_vers_nx("./data.json")

def dessiner_graph(G:dict):
    pos = nx.fruchterman_reingold_layout(G, k=2)
    nx.draw(G, pos=nx.circular_layout(G), with_labels= False,node_size= 50,node_color= "lightgreen",font_size = 10,linewidths = 2)
    plt.show()

def collaborateurs_communs(G:dict,u:str,v:str):
    """renvoie l'ensemble des collaborateurs en commun des deux acteurs

    Args:
        G (dict): le graphe
        u (str): un acteur
        v (str): un autre acteur

    Returns:
        set: ensemble des collaborateurs en communs
    """
    return nx.common_neighbors(G,u,v)

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