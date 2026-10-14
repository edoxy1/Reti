import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import scipy as sp
import scipy.sparse

# Posiziona la working directory nella stessa cartella in cui si trova lo script Python
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PDF_NAME = "karate_er_grafici.pdf"

# 1. Carichiamo la rete del Karate dal file edges.csv
G = nx.read_edgelist("edges.csv", delimiter=",", nodetype=int)

# 2. Calcolo nodi e link
print(f"Numero di nodi: {G.number_of_nodes()}")
print(f"Numero di link: {G.number_of_edges()}")

# 3. Matrice di adiacenza
adj_matrix = nx.to_numpy_array(G, nodelist=sorted(G.nodes()))
print(f"Dimensioni Matrice di Adiacenza: {adj_matrix.shape}")

# 4. Matrice di incidenza (Nodi x Archi)
incidence_matrix = nx.incidence_matrix(
    G, nodelist=sorted(G.nodes()), oriented=False
).toarray()
print(f"Dimensioni Matrice di Incidenza: {incidence_matrix.shape}")

# 5. Distribuzione del grado
degrees = [d for n, d in G.degree()]
degree_counts = np.bincount(degrees)
print("\nDistribuzione del grado (Grado -> Numero di nodi):")
for deg, count in enumerate(degree_counts):
    if count > 0:
        print(f"Grado {deg}: {count} nodi")


def disegna_grafo(graph, color, title, with_labels=True, node_size=500,
                  figsize=(8, 6), degree_counts=None):
    """Grafo a sinistra e, se richiesto, istogramma del grado a destra."""
    if degree_counts is not None:
        fig, (ax_graph, ax_hist) = plt.subplots(1, 2, figsize=(14, 6))
    else:
        fig, ax_graph = plt.subplots(figsize=figsize)
        ax_hist = None

    # Grafo (a sinistra)
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, ax=ax_graph, with_labels=with_labels, node_color=color,
            edge_color='gray', node_size=node_size, font_size=10)
    ax_graph.set_title(title)

    # Istogramma (a destra)
    if ax_hist is not None:
        ax_hist.bar(range(len(degree_counts)), degree_counts,
                    color='orange', edgecolor='black')
        ax_hist.set_xlabel("Grado k di un nodo (quanti link ha)")
        ax_hist.set_ylabel("Quanti nodi hanno quel grado")
        ax_hist.set_title("Distribuzione del grado")
        ax_hist.grid(axis='y', linestyle='--', alpha=0.7)

    fig.tight_layout()
    return fig


with PdfPages(PDF_NAME) as pdf:

    # --- Pagina 1: distribuzione del grado ---
    fig = plt.figure(figsize=(8, 4))
    plt.bar(range(len(degree_counts)), degree_counts, color='orange', edgecolor='black')
    plt.xlabel("Grado k di un nodo (quanti link ha)")
    plt.ylabel("Quanti nodi hanno quel grado")
    plt.title("Distribuzione del Grado - Zachary's Karate Club")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    pdf.savefig(fig)
    plt.close(fig)

    # --- Pagina 2: grafo del Karate Club ---
    fig = disegna_grafo(G, 'lightblue', "Grafo del Karate Club")
    pdf.savefig(fig)
    plt.close(fig)

    # --- Grafi di Erdős-Rényi ---
    print("\n--- GENERAZIONE GRAFI DI ERDŐS-RÉNYI ---")

    # Prova 1: pochi nodi, probabilità media
    n = 10000
    n1, p1 = n, 0.05
    ER1 = nx.erdos_renyi_graph(n1, p1, seed=1)
    degrees = [d for n, d in ER1.degree()]
    degree_counts = np.bincount(degrees)
    print(f"Prova 1 -> Nodi: {n1}, Probabilità: {p1} | Archi generati: {ER1.number_of_edges()}")
    fig = disegna_grafo(ER1, 'lightgreen', f"Grafo Erdős-Rényi G({n1}, {p1})", degree_counts=degree_counts)
    pdf.savefig(fig)
    plt.close(fig)

    # Prova 2: stesso n, probabilità più alta (rete più densa)
    n2, p2 = n, 0.15
    ER2 = nx.erdos_renyi_graph(n2, p2, seed=2)
    degrees = [d for n, d in ER2.degree()]
    degree_counts = np.bincount(degrees)
    print(f"Prova 2 -> Nodi: {n2}, Probabilità: {p2} | Archi generati: {ER2.number_of_edges()}")
    fig = disegna_grafo(ER2, 'lightcoral', f"Grafo Erdős-Rényi G({n2}, {p2})", degree_counts=degree_counts)
    pdf.savefig(fig)
    plt.close(fig)

    # Prova 3: più nodi, probabilità bassa
    n3, p3 = n, 0.40
    ER3 = nx.erdos_renyi_graph(n3, p3, seed=3)
    degrees = [d for n, d in ER3.degree()]
    degree_counts = np.bincount(degrees)
    print(f"Prova 3 -> Nodi: {n3}, Probabilità: {p3} | Archi generati: {ER3.number_of_edges()}")
    fig = disegna_grafo(ER3, 'lightblue', f"Grafo Erdős-Rényi G({n3}, {p3})",
                        with_labels=False, node_size=50, degree_counts=degree_counts)
    pdf.savefig(fig)
    plt.close(fig)

print(f"\nTutte le figure sono state salvate in '{PDF_NAME}'")