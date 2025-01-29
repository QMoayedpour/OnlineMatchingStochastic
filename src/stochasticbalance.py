import random

class StochasticBalance:
    def __init__(self, edges):
        self.u_edges = [edge[0] for edge in edges]
        self.loads = {}
        for u in self.u_edges:
            self.loads[u] = 0
        self.loads["nill"] = 0

    def filter_edges(self, edges, success):
        return [edge for edge in edges if edge[1] not in success]

    def __call__(self, v, edges, set_u=None):

        edges = self.filter_edges(edges, set_u)
        selected_u, prob = find_min_load(self.loads, edges)
        self.loads[selected_u] += prob

        success = random.uniform(0, 1) < prob

        if success and selected_u != "nill" and selected_u not in set_u:
            return selected_u

        return None


def find_min_load(loads, edges):
    selected_u, prob = min(
        ((u, score) for v, u, score in edges if u in loads),
        key=lambda x: (loads[x[0]], -x[1]),
        default=("nill", 0)
    )
    return (selected_u, prob)
