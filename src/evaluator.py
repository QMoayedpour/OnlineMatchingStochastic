import random
import networkx as nx
from src.opt import BudgetedAllocationSolver


class OnlineMatchingEvaluator:
    def __init__(self, algorithm, graph, edges):
        """
        :param model: Un modèle qui prend en entrée un noeud v et ses arêtes et renvoie un noeud u.
        :param graph: Un graphe biparti NetworkX avec des poids sur les arêtes.
        """
        self.algorithm = algorithm
        self.graph = graph
        self.score = 0
        self.matched = set()
        self.opt_calculator = BudgetedAllocationSolver(graph, edges)
        _, self.opt = self.opt_calculator.run()

        self.successful_assignments = {}

    def run(self):
        """ Execute l'évaluation en soumettant chaque v séquentiellement au modèle.
        :return score: Nombre de match par le modèle """
        self.score = 0
        V = [node for node, data in self.graph.nodes(data=True) if data['bipartite'] == 1]

        for v in V:
            edges = [(v, u, self.graph[v][u]['weight']) for u in self.graph.neighbors(v)]
            
            if not edges:
                continue

            chosen_u = self.algorithm(v, edges, self.successful_assignments)

            if chosen_u:
                self.score += 1
                self.matched.add((v, chosen_u))
                self.successful_assignments[chosen_u] = True 

        return self.score
