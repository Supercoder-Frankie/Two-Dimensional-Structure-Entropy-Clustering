#-*-coding: utf-8 -*-
#-*-author: liujun-*-

import random

"""
使用python实现PA model的生成器，使用邻接表数据结构存储生成的图,使用数字表示节点
邻接表格式：{node1: {node2: weight12, node3: weight13}, node2: {}}
嵌套的两层字典，第一层字典中的key表示图中的节点，比如v，value表示该节点v的邻居关系，
也用字典表示，key表示邻居节点u，value表示与该邻居的重边数.

input: n （表示模型网络的规模）
       d  (表示新加一个点需要连接d条边，默认是2，可以修改)
"""

def PA_Model_Generator(n, d=2):
	# 初始两个节点，节点ID分别为1和2
	adjacency_table = {1: {2: 1}, 2: {1: 1}}

	# 存储随机选出来的节点
	selected_nodes = []

	# 存储用于proportional to degree的列表，如下为初始情况
	repeated_nodes = [1, 2]

	# 初始新加的节点ID为3，node_id表示新加入的节点标号
	new_node_id = 3

	while new_node_id <= n:

		# 使用random的sample函数来随机获取d个节点，selected_nodes 为一个长度为 d 列表
		selected_nodes = random.sample(repeated_nodes, d)

		# 初始化新节点 new_node_id 的邻接表，表示即将与已有的节点建立连接关系
		adjacency_table.update({new_node_id: {}})

		# 更新邻接表和repeated_nodes列表，接下来需要自己实现
		# 对于更新邻接表，我们将新的 new_node_id 加到选出来的节点（selected_nodes）的邻居中，同时也将selected_nodes中的节点加到 
		# new_node_id 的邻居中。对于更新 repeated_nodes，我们在里面加入d个新的节点 new_node_id，同时把selected_nodes中的点都加进去
                
		for neighbor in selected_nodes:
			adjacency_table[neighbor].update({new_node_id: 1})
			adjacency_table[new_node_id].update({neighbor: 1})

		repeated_nodes.append(new_node_id)

		for node in selected_nodes:
			repeated_nodes.append(node)

		
		new_node_id += 1

	return adjacency_table
		

"""
函数功能：将生成的邻接表输出到文件
图文件的格式：节点1+分隔符(空格或制表符)+节点2+(权重)
input：adjacency_table 为存储图的邻接表
          file_path 是要存储的文件的路径
"""
def write_to_file(adjacency_table, file_path):
	graph_file = open(file_path, 'w')
	for node_id in range(1, n+1):
		for neighbor, weight in adjacency_table[node_id].items():
			if node_id < neighbor:
				graph_file.write(str(node_id)+' '+str(neighbor)+' '+str(weight)+'\n')
	graph_file.close()


# example
if __name__ == "__main__":
        import os # 引入操作系统库
        path = os.path.join(os.getcwd(), 'PA_model_example.txt') # 第二个字符串中为输出的文件名，可以自行设定
        n = 1000 # n 表示生成的网络模型的规模，这里为1000，可以修改
        adjacency_table = PA_Model_Generator(n) # 调用PA模型生成器，输出邻接表
        write_to_file(adjacency_table, path) # 调用函数将图存储到指定的路径  path 上
