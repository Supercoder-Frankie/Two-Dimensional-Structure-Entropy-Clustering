# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
from Graph import ResolveGraphFile as RGF


graph_path = 'Homophyly_model_example.txt' # 输入存储图的文件路径
# community = ['3', '2', '5', '28', '6', '7', '11', '31', '18', '44', '916', '202', '59', '37', '326', '116', '334', '88', '34', '115'] # 算法找出来的社区列表
# community = ['3', '2', '5', '28', '6', '7', '11', '31', '18', '44', '916', '202', '59', '37', '326', '116', '334', '88', '34', '115', '19', '567', '32', '67', '73', '335', '36', '51', '81', '483', '295', '74', '101', '14', '277', '733', '58', '42', '119', '367', '581', '294', '131', '469', '799', '439', '974', '248', '129', '818']
#community = ['3', '916', '2', '5', '28', '6', '7', '11', '31', '18', '44', '202', '59', '37', '326', '116', '334', '88', '34', '115']
community = ['3', '2', '28', '251', '253', '74', '760', '483', '367', '50', '335', '51', '119', '81', '49', '733', '818', '428', '501', '581']
adjacency_table = RGF(graph_path, weighted=False, sep=" ")

edges = []

for node in adjacency_table:
    for neighbor in adjacency_table[node]:
        if int(node) < int(neighbor):
            edges.append((node, neighbor))

G = nx.Graph(directed=False)
G.add_edges_from(edges)
position = nx.spring_layout(G)
plt.figure(figsize=(30,20))
nx.draw(G, pos=position, with_labels=False)

nx.draw_networkx_nodes(G, pos=position, nodelist=G.nodes(), node_size=300)

nx.draw_networkx_nodes(G, pos=position, nodelist=community, node_color='red', node_size=800)

plt.show()
# plt.savefig("result.png")
