class NonAdaptive:
    def __init__(self, edges):
        self.u_edges = [edge[0] for edge in edges]
        self.w = {}
        for u in self.u_edges:
            self.w[u] = 0

    def find_max_u(self, p):

        return max((u for v0, u, p_value in p if u in self.w), 
                key=lambda u: (1 - self.w[u]) * next(p_value for v0, u2, p_value in p if u == u2),
                default=None)

    def __call__(self, v, edges, set_u=None):

        selected_u = self.find_max_u(edges)

        self.w[selected_u] = self.w[selected_u] + (1-self.w[selected_u])*get_weight_for_u(edges, selected_u)
        return selected_u


def get_weight_for_u(p, u):
    for v0, current_u, weight in p:
        if current_u == u:
            return weight
    return None
