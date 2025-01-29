from collections import defaultdict
import numpy as np
from tqdm import tqdm
from src.utils import generate_bipartite_erdos_graph
from src.evaluator import OnlineMatchingEvaluator


def eval_benchmark(args):
    all_results = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    for p_value in tqdm(args["p_values"]):
        for u_n in args["U_n"]:

            p_erd_mapping = {
                "n": 1/u_n,
                "logn/n": np.log(u_n) / u_n
            }

            for p_erd in args["p_erd"]:
                p_erd_ = p_erd_mapping.get(p_erd, p_erd)

                B, edges = generate_bipartite_erdos_graph(u_n, u_n, p=p_value,
                                                          p_erd=p_erd_, p_max=args["p_max"])

                for algo, name in zip(args["algos"], args["names"]):
                    evaluator = OnlineMatchingEvaluator(algo(edges), B, edges)

                    scores = [evaluator.run() / evaluator.opt for _ in range(args["k"])]
           
                    all_results[p_value][u_n][p_erd][name] = sum(scores) / len(scores)

    return all_results
