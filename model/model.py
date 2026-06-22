from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapConstructor = {}


    def buildGraph(self,a1,a2):
        self._graph.clear()
        print(self._graph)
        self._addNodes(a1,a2)
        print(self._graph)
        self._addEdges(a1,a2,self._idMapConstructor)
        print(self._graph)

    def _addNodes(self,a1,a2):
        allNodes = DAO.getAllNodes(a1,a2)
        for n in allNodes:
            self._idMapConstructor[n.constructorId] = n
        self._graph.add_nodes_from(allNodes)
        return

    def _addEdges(self,a1,a2,idMapC):
        allEdges = DAO.getAllEdges(a1,a2,idMapC)
        for e in allEdges:
            self._graph.add_edge(e.c1,e.c2,weight=e.weight)
        return

    def topTreArchi(self):
        listaArchi = list(self._graph.edges(data = True))
        listaArchi.sort(key=lambda x:x[2]["weight"],reverse=True)
        return listaArchi

    def getNumCompConn(self):
        return nx.number_connected_components(self._graph)

    def getMaxCC(self):
        compMax = []
        for n in self._graph.nodes():
            if len(nx.node_connected_component(self._graph,n)) > len(compMax):
                compMax = list(nx.node_connected_component(self._graph,n))
        compMax.sort(key=lambda x:self._graph.degree(x),reverse=True)
        return compMax




    def getAllYears(self):
        return DAO.getAllYears()
