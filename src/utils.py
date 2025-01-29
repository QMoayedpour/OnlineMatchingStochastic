import networkx as nx
import random
import numpy as np
import pandas as pd


def generate_bipartite_erdos_graph(n_U=10, n_V=10, p_erd=0.3, p="random", factor=1, p_max=0.8):
    """
    Génère un graphe biparti de type Erdős-Rényi.
    :param n_U: Nombre de sommets dans le premier ensemble (U).
    :param n_V: Nombre de sommets dans le second ensemble (V).
    :param p_erd: Probabilité qu'une arête existe entre un sommet de U et un sommet de V.
    :param p: Probabilité de match entre deux arête u et v (si sélectionnés)
    :param factor: Augmenter ou diminuer p (quand généré aléatoirement)
    :return: Graphe biparti (NetworkX Graph) et la liste des arêtes avec leurs poids.

    """

    B = nx.Graph()

    U = [f"u{i}" for i in range(n_U)]
    V = [f"v{j}" for j in range(n_V)]
    B.add_nodes_from(U, bipartite=0)
    B.add_nodes_from(V, bipartite=1)

    edges = []
    for u in U:
        for v in V:
            if random.random() < p_erd:
                if p == "random":
                    weight = round(min(random.uniform(1e-5, p_max)*factor, 1), 2)
                else:
                    assert isinstance(p, float)
                    weight = p
                B.add_edge(u, v, weight=weight)
                edges.append((u, v, weight))
    isolated_nodes = list(nx.isolates(B))
    B.remove_nodes_from(isolated_nodes)
    return B, edges


def results_to_df(results):
    data = []
    
    for p_value, u_n_dict in results.items():
        for u_n, p_erd_dict in u_n_dict.items():
            for p_erd, scores in p_erd_dict.items():
                row = (p_value, u_n, p_erd) + tuple(scores.values())
                data.append(row)

    columns = ["p_value", "U_n", "p_erd"] + list(results[next(iter(results))][next(iter(results[next(iter(results))]))][next(iter(results[next(iter(results))][next(iter(results[next(iter(results))]))]))].keys())
    
    df = pd.DataFrame(data, columns=columns)
    df.set_index(["p_value", "U_n", "p_erd"], inplace=True)
    
    return df