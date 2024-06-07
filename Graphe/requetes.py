import networkx as nx
import matplotlib.pyplot as plt
import json
import customtkinter


from customtkinter import filedialog

def json_vers_nx(chemin:str): #O(n³)
    """Creer une liste de films

    Args:
        chemin (str): le chemin d'un fichier

    Returns:
        list: une liste de films
    """
    G = nx.Graph()
    
    with open(chemin, 'r', encoding='utf-8') as fichier:
        data = [json.loads(line.strip()) for line in fichier]
    print(data)
    for film in data:
        print(film ,"\n","\n")
        cast = [acteur.replace("[[", "").replace("]]", "") for acteur in film['cast']]
        for acteur in cast:
            if acteur not in G.nodes():
                G.add_node(acteur)

        for i in range(len(cast)):
            for j in range(i +1, len(cast)):
                if not G.has_edge(cast[i], cast[j]):
                    G.add_edge(cast[i], cast[j])
    
    return G

def collaborateurs_communs(G, u: str, v: str):
    """Renvoie l'ensemble des collaborateurs en commun des deux acteurs

    Args:
        G (dict): le graphe
        u (str): un acteur
        v (str): un autre acteur

    Returns:
        set: ensemble des collaborateurs en communs
    """
    voisins_u = set(nx.neighbors(G,u))
    print(voisins_u)
    voisins_v = set(nx.neighbors(G,v))
    print(voisins_v)
    return voisins_u.intersection(voisins_v)


def collaborateurs_proches(G: dict, u: str, k: int): #O(N³)
    """Fonction renvoyant l'ensemble des acteurs à distance au plus k de l'acteur u dans le graphe G. La fonction renvoie None si u est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        k: la distance depuis u
    """
    if u not in G:
        print(u, "est un illustre inconnu")
        return None

    collaborateurs = set([u])
    niveau_actuel = set([u])

    for _ in range(k):
        prochain_niveau = set()
        for acteur in niveau_actuel:
            for voisin in G[acteur]:
                if voisin not in collaborateurs:
                    prochain_niveau.add(voisin)
        collaborateurs.update(prochain_niveau)
        niveau_actuel = prochain_niveau

    return collaborateurs


def est_proche(G: dict, u: str, v: str, k: int = 1): #O(N³)
    """Permet de savoir si un collaborateur v est à distance k d'un acteur u

    Args:
        G (dict): le graphe
        u (str): un acteur
        v (str): un collaborateur
        k (int, optional): la distance. Defaults to 1.

    Returns:
        bool: True si le collaborateur se trouve a distance k d'un acteur sinon False
    """
    return v in collaborateurs_proches(G, u, k)


def distance_naive(G: dict, u: str, v: str): #O(N³)
    """Permet de déterminer la distance entre deux acteurs

    Args:
        G (dict): un graphe
        u (str): un acteur
        v (str): un autre acteur

    Returns:
        int: la distance entre deux acteurs
    """
    k = 1
    while v not in collaborateurs_proches(G, u, k):
        k += 1
    return k


def distance(G: dict, u: str, v: str):
    """Permet de déterminer la distance entre deux acteurs

    Args:
        G (dict): un graphe
        u (str): un acteur
        v (str): un autre acteur

    Returns:
        int: la distance entre deux acteurs
    """
    from collections import deque

    if u not in G or v not in G:
        return float('inf')

    queue = deque([(u, 0)])
    visités = set()

    while queue:
        current_node, current_distance = queue.popleft()
        if current_node == v:
            return current_distance
        visités.add(current_node)
        for voisin in G[current_node]:
            if voisin not in visités:
                queue.append((voisin, current_distance + 1))
                visités.add(voisin)

    return float('inf')


def centralite(G: dict, u: str):
    """Permet d'avoir la plus grande distance qui sépare un acteur donnée en paramètre d'un autre acteur

    Args:
        G (dict): un graphe
        u (str): un acteur

    Returns:
        int: la plus grande distance qui le sépare d'un autre acteur
    """
    from collections import deque

    if u not in G:
        return float('inf')

    queue = deque([(u, 0)])
    distances = {u: 0}

    while queue:
        current_node, current_distance = queue.popleft()
        for voisin in G[current_node]:
            if voisin not in distances:
                distances[voisin] = current_distance + 1
                queue.append((voisin, current_distance + 1))

    return max(distances.values())


def centre_hollywood(G: dict):
    """Permet d'avoir l'acteur le plus central d'un graphe

    Args:
        G (dict): un graphe

    Returns:
        str: l'acteur le plus central
    """
    centralites = {actor: centralite(G, actor) for actor in G.nodes}
    return max(centralites, key=centralites.get)


def eloignement_max(G: dict):
    """Permet d'avoir la distance maximum entre toutes les paires d'acteurs

    Args:
        G (dict): un graphe

    Returns:
        int: la distance maximum entre toutes les paires d'acteurs du graphe
    """
    def composants_connexes(G):
        visités = set()
        composantes = []

        for sommet in G:
            if sommet not in visités:
                composante = []
                stack = [sommet]
                while stack:
                    noeud = stack.pop()
                    if noeud not in visités:
                        visités.add(noeud)
                        composante.append(noeud)
                        stack.extend(G[noeud])
                composantes.append(composante)
        return composantes

    largest_cc = max(composants_connexes(G), key=len)
    subgraph = {node: G[node] for node in largest_cc}
    
    distances_max = {actor: centralite(subgraph, actor) for actor in subgraph}
    return max(distances_max.values())


# Q bonus

def centralite_groupe(G,S):
    ...