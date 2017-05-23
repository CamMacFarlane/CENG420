# Must have networkx installed to generate graph
# Use 'sudo pip install networkx' 
# NetworkX does not work with Python 3

import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edge('A', 'B', weight = 4)
G.add_edge('B', 'D', weight = 2)
G.add_edge('A', 'C', weight = 3)
G.add_edge('C', 'D', weight = 4)

nx.draw_random(G)
plt.show()

y = nx.shortest_path(G, 'A', 'D', weight='weight')
print y
