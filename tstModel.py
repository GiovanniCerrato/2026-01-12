from model.model import Model

m = Model()
m.buildGraph(2007,2009)
print(m.topTreArchi())
print(m.getNumCompConn())
print(m.getMaxCC())