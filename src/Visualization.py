from pyvis.network import Network
import pandas as pd

# 读取数据
dolphins_data = pd.read_csv('DataSet/dolphins.csv', sep='\t', header=None)
edges = dolphins_data.values.tolist()

# 创建网络
net = Network(notebook=True)

# 添加节点，确保设置了标签
for node in range(1, max(dolphins_data.max())+1):
    net.add_node(node, label=str(node))  # 节点编号作为标签

# 添加边
for edge in edges:
    net.add_edge(edge[0], edge[1])
# 设置网络的一些可选参数
net.set_options("""
var options = {
  "nodes": {
    "color": {
      "border": "rgba(255,255,255,1)",
      "background": "rgba(97,195,238,1)",
      "highlight": {
        "border": "rgba(255,255,255,1)",
        "background": "rgba(97,195,238,1)"
      }
    }
  },
  "edges": {
    "color": {
      "color": "rgba(97,195,238,1)",
      "highlight": "rgba(97,195,238,1)",
      "hover": "rgba(97,195,238,1)",
      "inherit": true,
      "opacity": 1.0
    }
  },
  "interaction": {
    "hover": true,
    "multiselect": true,
    "navigationButtons": true
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -80000,
      "centralGravity": 0.3,
      "springLength": 95
    },
    "minVelocity": 0.75
  }
}
""")

# 生成网络图
net.show('dolphins_network.html')

"""# 创建一个空的网络图
G = nx.Graph()

# 从CSV文件中读取数据
dolphins_data = pd.read_csv('DataSet/dolphins.csv',sep = '\t' , header=None, names=['Node1', 'Node2'])

# 添加边到网络图
for index, row in dolphins_data.iterrows():
    G.add_edge(row['Node1'], row['Node2'])

# 绘制网络图
plt.figure(figsize=(12, 8))
nx.draw(G, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray')
plt.title("Network Graph of Dolphins Relationships")
plt.show()
"""
