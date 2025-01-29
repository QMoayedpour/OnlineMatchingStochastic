import random
import networkx as nx
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpContinuous, PULP_CBC_CMD


class BudgetedAllocationSolver:
    def __init__(self, graph, edges):
        """
        :param graph: Graphe biparti NetworkX.
        :param edges: Liste des edges (u, v, poids).
        """
        self.graph = graph
        self.edges = {(u, v): w for u, v, w in edges}

        self.U = {n for n, d in graph.nodes(data=True) if d["bipartite"] == 0}
        self.V = {n for n, d in graph.nodes(data=True) if d["bipartite"] == 1}

    def run(self):
        """
        On utilise le package pulp en précisant les contraintes pour résoudre le probleme
        de budgeted allocation"""

        prob = LpProblem("Budgeted_Allocation", LpMaximize)

        x = { (u, v): LpVariable(f"x_{u}_{v}", 0, 1, LpContinuous) for (u, v) in self.edges }

        for v in self.V:
            prob += lpSum(x[u, v] for u in self.U if (u, v) in self.edges) <= 1

        Lu = { u: lpSum(x[u, v] * self.edges[u, v] for v in self.V if (u, v) in self.edges) for u in self.U }

        Lu_capped = { u: LpVariable(f"Lc_{u}", 0, 1, LpContinuous) for u in self.U }
        
        for u in self.U:
            prob += Lu_capped[u] <= Lu[u]
            prob += Lu_capped[u] <= 1

        prob += lpSum(Lu_capped[u] for u in self.U)
        prob.solve(PULP_CBC_CMD(msg=False))

        allocation = {(u, v): x[u, v].varValue for (u, v) in self.edges if x[u, v].varValue > 0}
        utility = sum(Lu_capped[u].varValue for u in self.U)

        return allocation, utility
