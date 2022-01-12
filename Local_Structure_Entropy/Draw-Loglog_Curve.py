import matplotlib.pyplot as plt
import numpy as np
from Graph import ResolveGraphFile as RGF
import math


graph_path = 'com-amazon.subungraph.txt'  # 把代码生成好的图的文件路径替换 'PA_model_example.txt'


adj = RGF(graph_path, weighted=False, sep="\t")


deg_nodeNum = {}
for node in adj:
    deg = 0
    for neighbor, weight in adj[node].items():
        deg += weight
    if deg not in deg_nodeNum:
        deg_nodeNum[deg] = 1
    else:
        deg_nodeNum[deg] += 1

x, y = [], []
for deg in sorted(deg_nodeNum.keys()):
    x.append(math.log(deg, 2))
    y.append(math.log(deg_nodeNum[deg], 2))



plt.figure()
plt.title('Com-Amazon')
plt.plot(x, y, 'o', color='red')
plt.show() # 把画好的图马上展示出来

# 把画好的图存到一个文件中，参数为文件的路径
# plt.savefig(r'test.jpg')
