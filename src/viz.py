import matplotlib.pyplot as plt
import networkx as nx


def plot_bipartite_graph(graph, U, V, save_fig=False, disp=False):

    pos = nx.drawing.layout.bipartite_layout(graph, nodes=U)

    plt.figure(figsize=(12, 5))
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=["skyblue" if node in U else "lightgreen" for node in graph.nodes],
        node_size=800,
        edge_color="gray",
        font_size=10,
    )

    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)

    plt.title("", fontsize=14)
    if save_fig:
        plt.savefig(save_fig)
    if disp:
        plt.show()

