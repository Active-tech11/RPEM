from collections import defaultdict
import pandas as pd
from SearchKNe import read_edges_from_csv
import networkx as nx


def read_common_neighbors_from_csv(file_path):
    common_neighbors_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            edge_nodes = parts[0].split(',')  # 分割 '14,18' 为 '14' 和 '18'
            edge = (int(edge_nodes[0]), int(edge_nodes[1]))  # 将分割后的字符串转换为整数
            neighbors = set(map(int, parts[1:]))  # 将邻居节点转换为整数
            common_neighbors_dict[edge] = neighbors
    return common_neighbors_dict

def save_paths_to_csv(paths, file_path):
    with open(file_path, 'w') as file:
        for path in paths:
            file.write(','.join(map(str, path)) + '\n')


def find_three_order_common_neighbors(G , node1 , node2) :
    # 找到两个节点的三阶邻居
    neighbors1 = set ( nx.single_source_shortest_path_length ( G , node1 , cutoff = 3 ).keys () )
    print ( f"{node1}的三阶邻居",neighbors1 )
    neighbors2 = set ( nx.single_source_shortest_path_length ( G , node2 , cutoff = 3 ).keys () )
    print ( f"{node2}的三阶邻居",neighbors2 )
    neighbors1.discard ( node1 )
    neighbors2.discard ( node2 )
    # 返回两者的交集
    # print ( neighbors1 & neighbors2 )
    return neighbors1 & neighbors2


def valid_paths(G , node1 , node2 , common_neighbors , max_path_length) :
    # 创建一个列表来存储所有有效路径
    valid_paths_list = []

    for path in nx.all_simple_paths ( G , source = node1 , target = node2 , cutoff = max_path_length ) :
        # 检查路径中是否至少包含一个三阶公共邻居
        if any ( neighbor in path for neighbor in common_neighbors ) :
            valid_paths_list.append ( path )

    valid_paths_list.sort ( key = len )

    return valid_paths_list


if __name__ == "__main__":
    edges_df = pd.read_csv( 'DataSet/dolphins_delete_target.csv' , header=None , sep= '\t' )
    edges = [tuple(x) for x in edges_df.values]
    G = nx.Graph()
    G.add_edges_from(edges)

    target_edges = read_edges_from_csv( 'DataSet/target_edges.csv' )
    #最大长度
    max_path_length = 6
    common_neighbors_file = 'DataSet/common_neighbors.csv'
    common_neighbors_dict = read_common_neighbors_from_csv(common_neighbors_file)

    for edge in target_edges:
        source_node, target_node = edge
        common_neighbors = common_neighbors_dict.get((source_node, target_node), set())

        all_valid_paths = valid_paths(G, source_node, target_node, common_neighbors, max_path_length)

        file_name = f"ComPath/{source_node},{target_node}.csv"
        save_paths_to_csv(all_valid_paths, file_name)
        print(f"Paths for edge {source_node}-{target_node} saved to {file_name}")
"""
def bfs_paths_including_common_neighbors(adj_list, start, goal, common_neighbors):
    queue = deque([(start, [start])])
    valid_paths = []

    while queue:
        vertex, path = queue.popleft()
        # 如果下一个节点是终点且路径包含公共邻居，记录这条路径
        if vertex == goal and any(cn in path for cn in common_neighbors):
            valid_paths.append(path)
            continue
        # 遍历邻接点
        for next_vertex in adj_list[vertex]:
            if next_vertex not in path:  # 避免环路
                queue.append((next_vertex, path + [next_vertex]))

    return valid_paths
'''
剪枝策略，只考虑路径长度不超过2k的
'''
def bfs_paths_with_pruning(adj_list, start, goal, max_length=13):
    queue = deque([(start, [start])])
    while queue:
        vertex, path = queue.popleft()
        if len(path) > max_length:
            continue  # 剪枝：如果路径已经超过最大长度，就不再扩展这条路径
        if vertex == goal:
            yield path
        for next_vertex in adj_list[vertex]:
            if next_vertex not in path:  # 防止环路
                queue.append((next_vertex, path + [next_vertex]))
                print(path)

def find_all_paths(adj_list, x, y, common_neighbors, max_length=13):
    all_paths = list(bfs_paths_with_pruning(adj_list, x, y, max_length))
    # 过滤出包含至少一个三阶公共邻居的路径
    valid_paths = [path for path in all_paths if any(neighbor in path[1:-1] for neighbor in common_neighbors)]
    print(valid_paths)
    return valid_paths


def dfs_paths(adj_list, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next_node in set(adj_list[vertex]) - set(path):
            if next_node == goal:
                yield path + [next_node]
            else:
                stack.append((next_node, path + [next_node]))

'''
直接查找所有路径，再按照是否包含公共邻居节点进行筛选
def find_paths_with_common_neighbors(adj_list, x, y, common_neighbors):
    all_paths = list(dfs_paths(adj_list, x, y))
    filtered_paths = [path for path in all_paths if any(neighbor in path for neighbor in common_neighbors)]
    filtered_paths.sort(key=len)  # 按路径长度升序排列
    return filtered_paths
'''
"""

"""edges = pd.read_csv(r'DataSet\dolphins.csv', header = None, sep = '\t').values
adj_list = build_adjacency_list(edges)

# 假设已经找到了x和y的共同三阶邻居
common_neighbors = find_common_neighbors(adj_list, 1, 9)
print(common_neighbors)
# 查找所有有效路径
paths = find_all_paths ( adj_list , 1 , 9 , common_neighbors , max_length = 13)
for path in paths :
    print("连通路径如下：" + ' -> '.join(map(str, path)))

 # 查找并排序包含共同邻居的路径
paths = find_paths_with_common_neighbors(adj_list, 1, 9, common_neighbors)
print(paths)

"""
