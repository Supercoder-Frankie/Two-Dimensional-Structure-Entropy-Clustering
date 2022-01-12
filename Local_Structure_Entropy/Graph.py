#-*- coding: utf-8 -*-
#-*- author: liujun-*-

import networkx as nx

"""
函数功能：将图文件转换成邻接表(适用于无向带权图)
图文件的格式：节点1+分隔符(空格或制表符)+节点2+(权重)
邻接表格式：{node1: {node2: weight12, node3: weight13}, node2: {}}
嵌套的两层字典，第一层字典中的key表示图中的节点，比如v，value表示该节点v的邻居关系，
也用字典表示，key表示邻居节点u，value表示与该邻居的权重w(u,v).
"""

def ResolveGraphFile(graph_path, weighted=True, sep='\t'):
    with open(graph_path) as graph_file:
        data = graph_file.readlines()
    adj_table = {}
    number_of_edges = 0
    
    for each_line in data:
        number_of_edges += 1
        column = each_line.strip().split(sep)
        node1, node2 = column[0], column[1]
        
        if weighted:
            weight = float(column[2])
        else:
            weight = 1
            
        if node1 not in adj_table:
            adj_table.update({node1: {node2: weight}})
        elif node2 not in adj_table[node1]:
            adj_table[node1].update({node2: weight})
        else:
            adj_table[node1][node2] += weight

        if node2 not in adj_table:
            adj_table.update({node2: {node1: weight}})
        elif node1 not in adj_table[node2]:
            adj_table[node2].update({node1: weight})
        else:
            adj_table[node2][node1] += weight
            
    print("number of vertices: ", len(adj_table))
    print("number of edges: ", number_of_edges)
    return adj_table

"""
函数功能：将图文件转换成networkx中图的数据结构
"""
def GraphStructure(graph_path, weighted=True, sep='\t'):
    with open(graph_path) as graph_file:
        data = graph_file.readlines()
    edges = []
    
    for line in data:
        column = line.strip().split(sep)
        node1, node2 = column[0], column[1]
        if weighted:
            edges.append((node1, node2, float(column[2])))
        else:
            edges.append((node1, node2))
            
    G = nx.Graph()
    if weighted:
        G.add_weighted_edges_from(edges)
    else:
        G.add_edges_from(edges)
    return G
