#-*- coding: utf-8 -*-

from Graph import ResolveGraphFile as RGF
import sys
import math


"""
实现局部结构熵挖掘社区的算法
输入为，start: 图的起始点

"""

"""
代码中所涉及到的变量名的含义
vol1： 表示社区 1 的体积
g1： 表示社区 1 的割边数目
vol2： 表示社区 2 的体积
g2： 表示社区 2 的割边数目
vol3： 表示合并后的社区 3 的体积
g3： 表示合并后的社区 3 的割边数目、
g12： 表示社区 1 和社区 2 之间的连边数目

"""

def Local_Structure_Entropy(graph_path, start, k=20):
        # 调用函数讲存储图的文件解析成用字典存的邻接表，用adjacency_table表示图的邻接表
        adjacency_table = RGF(graph_path, weighted=False, sep="\t")
        # 用字典存储每个节点的度数，key是节点ID，value是该节点的度数
        degree = {}
        # 存储所有度数的和
        m = 0
        # 计算每个节点的度数，以及所有节点度数之和
        for node in adjacency_table.keys():
                degree[node] = 0
                for neighbor, deg in adjacency_table[node].items():
                        m += deg
                        degree[node] += deg

        community = [start] # 存储社区节点的列表
        neighbors = {} # 当前社区的邻居字典集合

        vol1, g1 = 0.0, 0.0
        vol2, g2 = 0.0, 0.0
        vol3, g3 = 0.0, 0.0
        g12 = 0.0

        # 计算当前社区的邻居字典集合以及当前社区的体积与割边
        for neighbor, deg in adjacency_table[start].items():
                neighbors.update({neighbor: deg})
                vol1 += deg
                g1 += deg
        delta = 0.0

        # 1. 初始化，计算合并前后的结构熵的变化值delta
        # 初始化，计算合并前后的结构熵的变化值delta
        for node in neighbors: # 对于邻居中的每一个节点，选出结构熵变化最大的邻居节点与当前社区合并
                vol3 = vol1 + degree[node] # 合并后的社区体积
                g12 = 0.0
                g2 = degree[node]  # degree: 每个节点的度数
                neighbors_if_merge = {}
                for neighbor in adjacency_table[node]:  # 对于node的邻居
                        if neighbor in community:       # 如果node的邻居在社区里
                                g12 += adjacency_table[node][neighbor]   # 社区 1 和社区 2 之间的连边数目增加
                        else:
                                neighbors_if_merge.update({neighbor:adjacency_table[node][neighbor]})
                g3 = g1 + g2 - 2*g12    # 合并后的社区 3 的割边数目（外部 - 内部）
                
                # 计算并存下合并后结构熵变化的值
                item1 = (1/m)*(vol1*math.log(vol1, 2) - vol3*math.log(vol3, 2) - (g1*math.log(vol1, 2) - g3*math.log(vol3,2)))
                item2 = (1/m)*(2*g12*math.log(m, 2))
                delta_if_merge = item1 + item2

                # 存下结构熵变化最大的邻居节点
                if -delta_if_merge < delta:
                        delta = -delta_if_merge
                        com2 = [node]
                        vol3_after_merge = vol3
                        g3_after_merge = g3
                        neighbors_extra = neighbors_if_merge

        # 2. 合并delta最大的两个社区，以及更新相关的数据结构，包括社区列表，社区体积大小，
        # 割边数目，邻居集合等
        # 3. 继续尝试将社区的邻居加入到社区之中，并记下结构熵减小最大的邻居
        # 当社区的大小小于参数 k 时 并且 delta 小于 0 ，也就是说结构熵仍然在减小，
        # 否则循环继续执行。
        while len(community) < k and delta < 0.0:
                community.append(com2[0])  # 1. 更新社区体积大小
                del neighbors[com2[0]]

                for neighbor in adjacency_table[community[-1]].keys():  #更新邻居的集合
                        if neighbor in community:  # 如果node的邻居在社区里
                                g12 += adjacency_table[community[-1]][neighbor]  # 社区 1 和社区 2 之间的连边数目增加
                        else:
                                neighbors.update({neighbor: adjacency_table[community[-1]][neighbor]})  # 2. 邻居集合

                vol1 = vol3_after_merge  # 体积
                g1 = g3_after_merge  # 割边数目
                g12 = 0.0

                for node in neighbors:  # 对于邻居中的每一个节点，选出结构熵变化最大的邻居节点与当前社区合并
                        vol3 = vol3_after_merge + degree[node]  # 合并后的社区体积
                        g2 = degree[node]  # degree: 每个节点的度数
                        neighbors_if_merge = {}
                        for neighbor in adjacency_table[node]:  # 对于node的邻居
                                if neighbor in community:  # 如果node的邻居在社区里
                                        g12 += adjacency_table[node][neighbor]  # 社区 1 和社区 2 之间的连边数目增加
                                else:
                                        neighbors_if_merge.update({neighbor: adjacency_table[node][neighbor]})
                        g3 = g1 + g2 - 2 * g12  # 合并后的社区 3 的割边数目（外部 - 内部）

                        # 计算并存下合并后结构熵变化的值
                        item1 = (1 / m) * (vol1 * math.log(vol1, 2) - vol3 * math.log(vol3, 2) - (
                                        g1 * math.log(vol1, 2) - g3 * math.log(vol3, 2)))
                        item2 = (1 / m) * (2 * g12 * math.log(m, 2))
                        delta_if_merge = item1 + item2

                        # 存下结构熵变化最大的邻居节点
                        if -delta_if_merge < delta:
                                delta = -delta_if_merge
                                com2 = [node]
                                vol3_after_merge = vol3
                                g3_after_merge = g3
                                neighbors_extra = neighbors_if_merge


        # print(community, delta)
        return community, delta
        
        

                                        
# example
if __name__ == "__main__":
        file_name = "com-amazon.subungraph.txt" # 输入的图的文件名字
        start = '586'
        print(Local_Structure_Entropy(file_name, start))
        


