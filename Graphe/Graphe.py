import networkx as nx
import matplotlib.pyplot as plt
import json
from tkinter import *
from tkinter  import filedialog
import customtkinter

def json_vers_nx(chemin:str):
    """Creer une liste de films

    Args:
        chemin (str): le chemin d'un fichier

    Returns:
        list: une liste de films
    """
    G = nx.Graph()
    
    with open(chemin, 'r', encoding='utf-8') as fichier:
        data = [json.loads(line) for line in fichier]
    
    for film in data:
        cast = film['cast']
        for acteur in cast:
            G.add_node(acteur)
        for i in range(len(cast)):
            for j in range(i + 1, len(cast)):
                G.add_edge(cast[i], cast[j])
    
    return G

G = json_vers_nx("Graphe/data.txt")

def dessiner_graph(G:nx.Graph):
    """Permet d'afficher le graphe

    Args:
        G (nx.Graph): un graphe
    """
    pos = nx.fruchterman_reingold_layout(G, k=2)
    nx.draw(G, pos=nx.circular_layout(G), with_labels= False,node_size= 50,node_color= "lightgreen",font_size = 10,linewidths = 2)
    plt.show()

def collaborateurs_communs(G:nx.Graph,u:str,v:str):
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

def collaborateurs_proches(G:nx.Graph,u:str,k:int): #O(N³)
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


def est_proche(G:nx.Graph,u:str,v:str,k:int=1): #O(N³)
    """Permet de savoir si un collaborateur v est à distance k d'un acteur u

    Args:
        G (dict): le graphe
        u (str): un acteur
        v (str): un collaborateur
        k (int, optional): la distance. Defaults to 1.

    Returns:
        bool: True si le collaborateur se trouve a distance k d'un acteur sinon False
    """
    return v in collaborateurs_proches(G,u,k)
    
def distance_naive(G:nx.Graph,u:str,v:str): #O(N³)
    """Permet de déterminer la distance entre deux acteurs

    Args:
        G (nx.Graph): un graphe
        u (str): un acteur
        v (str): un autre acteur

    Returns:
        int: la distance entre deux acteurs
    """
    k=1
    while (u not in collaborateurs_proches(G,v,k)):
        k+=1
    return k

def distance(G:nx.Graph,u:str,v:str):
    """Permet de déterminer la distance entre deux acteurs

    Args:
        G (nx.Graph): un graphe
        u (str): un acteur
        v (str): un autre acteur

    Returns:
        int: la distance entre deux acteurs
    """
    return nx.shortest_path_length(G, u, v)


# Q4

def centralite(G:nx.Graph,u:str):
    """Permet d'avoir la plus grande distance qui sépare un acteur donnée en paramètre d'un autre acteur

    Args:
        G (nx.Graph): un graphe
        u (str): un acteur

    Returns:
        int: la plus grande distance qui le sépare d'un autre acteur
    """
    res = nx.single_source_shortest_path_length(G, u)
    return max(res.values())

def centre_hollywood(G:nx.Graph):
    """Permet d'avoir l'acteur le plus central d'un graphe

    Args:
        G (nx.Graph): un graphe

    Returns:
        str: l'acteur le plus central
    """
    return min((centralite(G, actor), actor) for actor in G.nodes())[1]

# Q5

def eloignement_max(G:nx.Graph):
    """Permet d'avoir la distance maximum entre toutes les paires d'acteurs

    Args:
        G (nx.Graph): un graphe

    Returns:
        int: la distance maximum entre toutes les paires d'acteurs du graphe
    """
    # le graphique pouvant ne pas etre connexe on prend le sous-graphe le plus grand
    largest_cc = max(nx.connected_components(G), key=len)
    subgraph = G.subgraph(largest_cc)
    
    eccentricity = nx.eccentricity(subgraph)
    return max(eccentricity.values())

print(eloignement_max(G))

# Q bonus

def centralite_groupe(G,S):
    ...




# Application
app = customtkinter.CTk()
app.geometry("400x150")

def parcourir_fichier():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))


app.mainloop()