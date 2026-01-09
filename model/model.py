from database.DAO import DAO
import networkx as nx
import copy
class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._constructors = []
        self._idMap = {}
        self._year1 = None
        self._year2 = None

        self._optListaCostruttori = None
        self._optScore = None

    def getYears(self):
        return DAO.getAllYears()

    def buildGraph(self, anno1, anno2):
        self._graph.clear()
        self._idMap.clear()
        self._year1 = anno1
        self._year2 = anno2

        self._constructors = DAO.getAllConstructorsByYearRange(anno1, anno2)
        for c in self._constructors:
            self._idMap[c.constructorId] = c

        self._graph.add_nodes_from(self._constructors)

        allEdges = DAO.getConstructorEdges(anno1, anno2, self._idMap)
        for e in allEdges:
                self._graph.add_edge(e[0], e[1], weight=e[2])

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getTop3Archi(self):
        return sorted(self._graph.edges(data=True), key=lambda e: e[2]['weight'], reverse=True)[:3]

    def getConnectedComponents(self):

        components = list(nx.connected_components(self._graph))
        largest = max(components, key=len)

        sub_graph = self._graph.subgraph(largest).copy()
        ordered_nodes = sorted(sub_graph.nodes(), key=lambda n: self._graph.degree(n), reverse=True)

        details = [f"{node} (grado={self._graph.degree(node)})" for node in ordered_nodes]

        return len(components), largest, details

    def getListaCostruttoriOttima(self, k):
        self._optListaCostruttori = []
        self._optScore = 365 * 100  # 100 years in days

        # Load oldest driver DOB for each constructor
        DAO.getOldestDriverPerConstructor(self._year1, self._year2, self._idMap)

        components = list(nx.connected_components(self._graph))

        if k > len(components):
            return None, 0

        parziale = []
        self._ricorsioneCostruttori(components, k, parziale, 0)
        return self._optListaCostruttori, self._optScore

    def _ricorsioneCostruttori(self, componenti, k, parziale, index_componente):
        # Base case: found k constructors
        if len(parziale) == k:
            # Check if all constructors have oldest_driver_dob
            dobs = [c.oldest_driver_dob for c in parziale if c.oldest_driver_dob is not None]
            if len(dobs) != k:
                return  # Skip if some constructors don't have data

            diff_attuale = (max(dobs) - min(dobs)).days

            if diff_attuale < self._optScore:
                self._optScore = diff_attuale
                self._optListaCostruttori = copy.deepcopy(parziale)
            return

        # Termination conditions
        if index_componente >= len(componenti):
            return
        if (len(componenti) - index_componente) < (k - len(parziale)):
            return

        # Option 1: Skip this component
        self._ricorsioneCostruttori(componenti, k, parziale, index_componente + 1)

        # Option 2: Choose one constructor from this component
        componente_corrente = componenti[index_componente]
        for costruttore in componente_corrente:
            if costruttore.oldest_driver_dob is not None:
                parziale.append(costruttore)
                self._ricorsioneCostruttori(componenti, k, parziale, index_componente + 1)
                parziale.pop()

