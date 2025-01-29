import random

class Baseline:
    def __init__(self, edges):
        pass
    def __call__(self, v, edges, set_u=None):
        v,u,p = max(edges, key=lambda e: e[2])

        if random.random() < p and u not in set_u:
            return u
        return None