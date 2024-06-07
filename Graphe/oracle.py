import customtkinter
from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt
from requetes import *

# Application
app = customtkinter.CTk()
app.geometry("600x400")
app.title("A la conquête d'Hollywood")
app.config(background="white")

# Créer un label
label_file_explorer = customtkinter.CTkLabel(app, text="Parcourir un fichier", width=100, height=4)

# Le controleur du bouton 
def parcourir_fichier():
    try:
        filename = filedialog.askopenfilename(initialdir=".", title="Select a File", filetypes=[("Text files", "*.txt*"), ("All files", "*.*")])
        label_file_explorer.configure(text="Fichier ouvert: " + filename)
        G = json_vers_nx(filename)
        dessiner_graph(G)
        activer_boutons()
        return G
    except Exception as e:
        label_file_explorer.configure(text="Impossible d'ouvrir le fichier. Mauvaises données.")
        print(e)

def dessiner_graph(G: nx.Graph):
    Gdt = nx.dfs_tree(G, centre_hollywood(G))
    plt.figure(figsize=(10, 7))
    nx.draw(Gdt, pos=nx.planar_layout(Gdt), with_labels=True, node_size=500, node_color="lightgreen", font_size=10, linewidths=2, edge_color="gray", font_color="black")
    plt.title("Graphe des acteurs d'Hollywood")
    plt.show()

# Activer les boutons dès qu'un bon fichier est chargé
def activer_boutons():
    button_communs.configure(state="normal")
    button_proches.configure(state="normal")
    button_distance.configure(state="normal")

# Ajout de boutons
def afficher_collaborateurs_communs():
    u = entry_actor1.get()
    v = entry_actor2.get()
    communs = collaborateurs_communs(G, u, v)
    label_result.configure(text=f"Collaborateurs communs entre {u} et {v}: {communs}")

def afficher_collaborateurs_proches():
    u = entry_actor1.get()
    k = int(entry_distance.get())
    proches = collaborateurs_proches(G, u, k)
    label_result.configure(text=f"Collaborateurs à distance {k} de {u}: {proches}")

def afficher_distance():
    u = entry_actor1.get()
    v = entry_actor2.get()
    dist = distance(G, u, v)
    label_result.configure(text=f"Distance entre {u} et {v}: {dist}")

button_parcourir = customtkinter.CTkButton(app, text="Parcourir", command=parcourir_fichier)
G = button_parcourir.cget("command")
button_exit = customtkinter.CTkButton(app, text="Quitter", command=exit)

entry_actor1 = customtkinter.CTkEntry(app, placeholder_text="Acteur 1")
entry_actor2 = customtkinter.CTkEntry(app, placeholder_text="Acteur 2")
entry_distance = customtkinter.CTkEntry(app, placeholder_text="Distance k")

button_communs = customtkinter.CTkButton(app, text="Collaborateurs Communs", command=afficher_collaborateurs_communs, state="disabled")
button_proches = customtkinter.CTkButton(app, text="Collaborateurs Proches", command=afficher_collaborateurs_proches, state="disabled")
button_distance = customtkinter.CTkButton(app, text="Distance", command=afficher_distance, state="disabled")

label_result = customtkinter.CTkLabel(app, text="Résultat")

button_parcourir.grid(column=1, row=1, padx=20, pady=10)
label_file_explorer.grid(column=1, row=2, padx=20, pady=5)
entry_actor1.grid(column=1, row=4, padx=20, pady=5)
entry_actor2.grid(column=1, row=5, padx=20, pady=5)
entry_distance.grid(column=1, row=6, padx=20, pady=5)
button_communs.grid(column=1, row=7, padx=20, pady=5)
button_proches.grid(column=1, row=8, padx=20, pady=5)
button_distance.grid(column=1, row=9, padx=20, pady=5)
label_result.grid(column=1, row=10, padx=20, pady=10)
button_exit.grid(column=1, row=11, padx=20, pady=20)

app.mainloop()
