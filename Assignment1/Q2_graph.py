# Must have networkx installed to generate graph
# Use 'sudo pip install networkx' 
# NetworkX does not work with Python 3

import networkx as nx
import matplotlib.pyplot as plt

# Generate graph and nodes
G = nx.Graph()
G.add_nodes_from(range(0,19))

# Node Labels
l = {   0:'Internet', 
        1:'Web App',
        2:'Email Phishing', 
        3:'Mobile App',
        4:'REST APIs',
        5:'Web Server (L)',
        6:'Web Server (R)',
        7:'Application Server',
        8:'VPN Access',
        9:'Email Access',
        10:'*Accounting*',
        11:'DMZ Network',
        12:'*Mail Server*',
        13:'DB Server',
        14:'Prinate Network',
        15:'*HR Server*',
        16:'LDAP Server',
        17:'*Workstations*',
        18:'*R&D Server*'      
    }

# Node Colouring
colours = ['r' for x in range(0,19)]
goal = '#fcc41b'
colours[10] = goal;
colours[12] = goal;
colours[15] = goal;
colours[17] = goal;
colours[18] = goal;

# Edge assignment

# 0: Internet
G.add_edge(0,1,weight=50)
G.add_edge(0,2,weight=40)
G.add_edge(0,3,weight=90)
G.add_edge(0,4,weight=70)

# 1: Web App
G.add_edge(1,5,weight=120)

# 2: Email Phishing
G.add_edge(2,8,weight=170)
G.add_edge(2,9,weight=200)

# 3: Mobile App
G.add_edge(3,7,weight=120)
G.add_edge(3,6,weight=20)

# 4: Rest APIs
G.add_edge(4,6,weight=0)

# 5: Web Server (left)
G.add_edge(5,7,weight=90)

# 6: Web Server (right)
G.add_edge(6,7,weight=100)

# 7: Application Server
G.add_edge(7,13,weight=330)
G.add_edge(7,11,weight=300)

# 8: VPN Access
G.add_edge(8,14,weight=120)

# 9: Email Access
G.add_edge(9,12,weight=356)

# 10: Accounting*

# 11: DMZ Network
G.add_edge(11,13,weight=30)
G.add_edge(11,14,weight=410)

# 12: Mail Server*

# 13: DB Server
G.add_edge(13,10,weight=610)

# 14: Private Network
G.add_edge(14,16,weight=710)
G.add_edge(14,15,weight=530)

# 15: HR Server*

# 16: LDAP Server
G.add_edge(16,17,weight=240)
G.add_edge(16,18,weight=830)

# 17: Workstations*

# 18: R&D Server*

# Draw and display graph (circular format to avoid random graph generation)
nx.draw_circular(G, labels=l, node_color=colours, node_size = 600)
plt.show()

