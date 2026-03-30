from pyvis.network import Network
import pandas as pd


dolphins_data = pd.read_csv('DataSet/dolphins.csv', sep='\t', header=None)
edges = dolphins_data.values.tolist()


net = Network(notebook=True)


for node in range(1, max(dolphins_data.max())+1):
    net.add_node(node, label=str(node))  


for edge in edges:
    net.add_edge(edge[0], edge[1])

net.set_options()


net.show('dolphins_network.html')

