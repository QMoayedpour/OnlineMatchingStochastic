import random
import numpy as np

class SemiAdaptative:
    def __init__(self, edges):
        self.u_edges = np.unique([edge[0] for edge in edges])
        self.w = {}
        self.first_success = {}
        self.has_been_selected = {}
        for u in self.u_edges:
            self.w[u] = 0
            self.first_success[u] = False
            self.has_been_selected[u] = False

    def __call__(self, v, edges, set_u=None):

        # Sort the u's by the weight of the edge
        u_edges_sorted = sorted(edges, key=lambda vup: (1 - self.w[vup[1]]) * get_weight_for_u(edges, vup[1]), reverse=True)
        
        # special case: only one u
        if len(u_edges_sorted) == 1:
            # v, u, p = u_edges_sorted[0]
            # if random.uniform(0, 1) < p:
            #     self.first_success[u] = True
            #     return u
            
            return None

        # Select the two first u's
        v1, u1, p1 = u_edges_sorted[0]
        v2, u2, p2 = u_edges_sorted[1]

        # Adaptive choice
        selected_u = None
        if not u1 is set_u:
            # if is sucess match u1 and v
            if random.uniform(0, 1) < p1:
                self.first_success[u1] = True
                selected_u = u1
        elif u1 in set_u and self.first_success[u1] == False:
            # simulate matching u1 and v
            if random.uniform(0, 1) < p1:
                self.first_success[u1] = True
        elif u1 in set_u and self.first_success[u1] == True and u2 not in set_u:
            # match u2 and v
           selected_u = u2

        # Non-adaptive updates
        self.w[u1] = self.w[u1] + (1 - self.w[u1]) * p1
        self.w[u2] = p2 * self.w[u1] + (1 - p2) * self.w[u2]

        return selected_u


def get_weight_for_u(p, u):
    for v0, current_u, weight in p:
        if current_u == u:
            return weight
    return 0
