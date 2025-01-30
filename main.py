import numpy as np
from src.utils import results_to_df
from src.viz import plot_bipartite_graph
from src.utils import generate_bipartite_erdos_graph
from src.nonadaptive import NonAdaptive
from src.stochasticbalance import StochasticBalance
from src.semiadaptative import SemiAdaptative
from src.baseline import Baseline, BaselineAdaptive
from src.benchmark import eval_benchmark


def main(plot=True):
    n_U, n_V = 20, 20

    B, edges = generate_bipartite_erdos_graph(n_U, n_V, p_erd=np.log(n_U)/n_U, p_max=0.1)

    U = [f"u{i}" for i in range(n_U)]
    V = [f"v{j}" for j in range(n_V)]

    plot_bipartite_graph(B, U, V, save_fig='./figs/graph_example.pdf')

    opt = {"algos": [Baseline, NonAdaptive, BaselineAdaptive, StochasticBalance, SemiAdaptative], # List des fonction de chaque algo
        "names": ['Naive', 'NonAdaptive', 'NaiveAdaptive', 'StochasticBalance', 'SemiAdaptative'],
        "p_values": ["random", 0.5, 0.1, 0.05], # Not the classical p values...
        "U_n": [20, 50, 150],
        "p_erd": [0.2, "n", "logn/n"],
        "k": 20,
        "p_max":0.1 # Proba max dans un edge dans le cas random
        }  

    results = eval_benchmark(opt)

    df_results = results_to_df(results)

    df_results.round(2).to_csv("./results.csv")

if __name__ == "__main__":
    main()
