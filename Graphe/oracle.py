import customtkinter
from tkinter import filedialog, Toplevel
import networkx as nx
import matplotlib.pyplot as plt
from requetes import *
import random

# Application
app = customtkinter.CTk()
app.geometry("1920x1080")
app.title("À la conquête d'Hollywood")
app.config(background="white")

# Créer un label
label_file_explorer = customtkinter.CTkLabel(app, text="Parcourir un fichier", width=100, height=4)

# Le contrôleur du bouton parcourir
def parcourir_fichier():
    try:
        filename = filedialog.askopenfilename(initialdir=".", title="Select a File", filetypes=[("Text files", "*.txt*"), ("All files", "*.*")])
        label_file_explorer.configure(text="Fichier ouvert: " + filename)
        global G
        G = json_vers_nx(filename)
        dessiner_graph(G)
        activer_boutons()
    except Exception as e:
        label_file_explorer.configure(text=f"Erreur: {e}")

def dessiner_graph(G: nx.Graph):
    Gdt = nx.dfs_tree(G)
    plt.figure(figsize=(10, 7))
    nx.draw(Gdt, pos=nx.planar_layout(Gdt), with_labels=True, node_size=500, node_color="lightgreen", font_size=10, linewidths=2, edge_color="gray", font_color="black")
    plt.title("Graphe des acteurs d'Hollywood")
    plt.savefig("graphe.svg")
    plt.show()

# Activer les boutons dès qu'un fichier est chargé
def activer_boutons():
    button_centre_hollywood.configure(state="normal")
    button_communs.configure(state="normal")
    button_proches.configure(state="normal")
    button_distance.configure(state="normal")

# Sélectionner un acteur au hasard
def choisir_acteur_aleatoire(entry):
    if G is not None:
        acteur_aleatoire = random.choice(list(G.nodes))
        entry.delete(0, 'end')
        entry.insert(0, acteur_aleatoire)

# Fonction pour ouvrir une fenêtre pop-up pour les collaborateurs communs
def popup_collaborateurs_communs():
    popup = Toplevel(app)
    popup.geometry("400x200")
    popup.title("Collaborateurs Communs")

    entry_actor1 = customtkinter.CTkEntry(popup, placeholder_text="Acteur 1")
    entry_actor1.grid(column=0, row=0, padx=20, pady=10)
    button_actor1 = customtkinter.CTkButton(popup, text="Choisir aléatoirement", command=lambda: choisir_acteur_aleatoire(entry_actor1))
    button_actor1.grid(column=1, row=0, padx=20, pady=10)

    entry_actor2 = customtkinter.CTkEntry(popup, placeholder_text="Acteur 2")
    entry_actor2.grid(column=0, row=1, padx=20, pady=10)
    button_actor2 = customtkinter.CTkButton(popup, text="Choisir aléatoirement", command=lambda: choisir_acteur_aleatoire(entry_actor2))
    button_actor2.grid(column=1, row=1, padx=20, pady=10)

    def submit():
        try:
            u = entry_actor1.get()
            v = entry_actor2.get()
            communs = collaborateurs_communs(G, u, v)
            label_result.configure(text=f"Collaborateurs communs entre {u} et {v} \n{communs}")
            popup.destroy()
        except Exception as e:
            label_result.configure(text=f"Erreur: {e}")

    button_submit = customtkinter.CTkButton(popup, text="Submit", command=submit)
    button_submit.grid(column=0, row=2, padx=20, pady=10)

# Fonction pour ouvrir une fenêtre pop-up pour les collaborateurs proches
def popup_collaborateurs_proches():
    popup = Toplevel(app)
    popup.geometry("400x200")
    popup.title("Collaborateurs Proches")

    entry_actor = customtkinter.CTkEntry(popup, placeholder_text="Acteur 1")
    entry_actor.grid(column=0, row=0, padx=20, pady=10)
    button_actor = customtkinter.CTkButton(popup, text="Choisir aléatoirement", command=lambda: choisir_acteur_aleatoire(entry_actor))
    button_actor.grid(column=1, row=0, padx=20, pady=10)

    entry_distance = customtkinter.CTkEntry(popup, placeholder_text="Distance")
    entry_distance.grid(column=0, row=1, padx=20, pady=10)

    def submit():
        try:
            u = entry_actor.get()
            k = int(entry_distance.get())
            proches = collaborateurs_proches(G, u, k)
            label_result.configure(text=f"Collaborateurs à distance {k} de {u} \n{proches}")
            popup.destroy()
        except Exception as e:
            label_result.configure(text=f"Erreur: {e}")

    button_submit = customtkinter.CTkButton(popup, text="Submit", command=submit)
    button_submit.grid(column=0, row=2, padx=20, pady=10)

# Fonction pour ouvrir une fenêtre pop-up pour la distance
def popup_distance():
    popup = Toplevel(app)
    popup.geometry("400x200")
    popup.title("Distance")

    entry_actor1 = customtkinter.CTkEntry(popup, placeholder_text="Acteur 1")
    entry_actor1.grid(column=0, row=0, padx=20, pady=10)
    button_actor1 = customtkinter.CTkButton(popup, text="Choisir aléatoirement", command=lambda: choisir_acteur_aleatoire(entry_actor1))
    button_actor1.grid(column=1, row=0, padx=20, pady=10)

    entry_actor2 = customtkinter.CTkEntry(popup, placeholder_text="Acteur 2")
    entry_actor2.grid(column=0, row=1, padx=20, pady=10)
    button_actor2 = customtkinter.CTkButton(popup, text="Choisir aléatoirement", command=lambda: choisir_acteur_aleatoire(entry_actor2))
    button_actor2.grid(column=1, row=1, padx=20, pady=10)

    def submit():
        try:
            u = entry_actor1.get()
            v = entry_actor2.get()
            dist = distance(G, u, v)
            label_result.configure(text=f"Distance entre {u} et {v} \n{dist}")
            popup.destroy()
        except Exception as e:
            label_result.configure(text=f"Erreur: {e}")

    button_submit = customtkinter.CTkButton(popup, text="Submit", command=submit)
    button_submit.grid(column=0, row=2, padx=20, pady=10)
    
def dessiner_centre_hollywood(G: nx.Graph):
    centre = centre_hollywood(G)
    Gdt = nx.dfs_tree(G, centre)
    plt.figure(figsize=(10, 7))
    nx.draw(Gdt, pos=nx.planar_layout(Gdt), with_labels=True, node_size=500, node_color="lightgreen", font_size=10, linewidths=2, edge_color="gray", font_color="black")
    plt.title("Graphe de l'acteur au centre d'Hollywood")
    plt.savefig(f"centre_hollywood_{centre}.svg")
    plt.show()

# Ajout de boutons
button_parcourir = customtkinter.CTkButton(app, text="Parcourir", command=parcourir_fichier)
button_exit = customtkinter.CTkButton(app, text="Quitter", command=exit)

button_communs = customtkinter.CTkButton(app, text="Collaborateurs Communs", command=popup_collaborateurs_communs, state="disabled")
button_proches = customtkinter.CTkButton(app, text="Collaborateurs Proches", command=popup_collaborateurs_proches, state="disabled")
button_distance = customtkinter.CTkButton(app, text="Distance", command=popup_distance, state="disabled")
button_centre_hollywood = customtkinter.CTkButton(app, text="Afficher Centre Hollywood", command=lambda: dessiner_centre_hollywood(G), state="disabled")

label_result = customtkinter.CTkLabel(app, text="Résultat")

button_parcourir.grid(column=1, row=1, padx=20, pady=10)
label_file_explorer.grid(column=1, row=2, padx=20, pady=5)
button_centre_hollywood.grid(column=1, row=3, padx=20, pady=5)
button_communs.grid(column=1, row=4, padx=20, pady=5)
button_proches.grid(column=1, row=5, padx=20, pady=5)
button_distance.grid(column=1, row=6, padx=20, pady=5)
label_result.grid(column=1, row=7, padx=20, pady=10)
button_exit.grid(column=1, row=8, padx=20, pady=20)

app.mainloop()