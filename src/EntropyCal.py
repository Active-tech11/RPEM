import math
import networkx as nx
import pandas as pd

from SearchConPath import valid_paths
from SearchKNe import find_common_neighbors, build_adjacency_list, read_edges_from_csv
from collections import defaultdict


def read_paths_from_csv(file_path):
    with open(file_path, 'r') as file:
        paths = [list(map(int, line.strip().split(','))) for line in file]
    return paths


def create_graph_from_adjacency_list(adj_list):
    G = nx.Graph ()
    for node , neighbors in adj_list.items () :
        for neighbor in neighbors :
            G.add_edge ( node , neighbor )
    return G


def calculate_total_signal_for_edge(adj_list, G, xi, yi, max_path_length):
    common_neighbors = find_common_neighbors(adj_list, xi, yi)
    paths = valid_paths(G, xi, yi, common_neighbors, max_path_length)
    total_signal = calculate_signal_strength(adj_list, paths)
    return total_signal


def calculate_signal_strength(adj_list , paths , xi , yi) :
    # 存储节点的累积信号量
    node_signals = defaultdict ( float )
    node_signals[xi] = 1.0  # 源节点的信号量设置为1

    # 按路径长度排序，以确保首先处理最短的路径
    paths.sort ( key = len )

    # 遍历每条路径
    for path in paths :
        signal = node_signals[path[0]]  # 从源节点获取信号量
        for i , node in enumerate ( path[1 :] , 1 ) :
            if i < len ( path ) - 1 :  # 不处理目标节点
                degree = len ( adj_list[node] )
                signal /= degree  # 分裂信号
            node_signals[node] +=  signal # 累加信号至节点

    # 最终目标节点 y 的信号量是所有路径上信号量的总和
    total_signal_at_y = node_signals[yi]
    return total_signal_at_y


def calculate_entropy_per_path(signal) :
    if signal > 0 :
        return -signal * math.log ( signal , 2 )
    else :
        return 0


def calculate_total_entropy(adj_list, paths, xi, yi):

    # 计算每条路径的信号强度
    path_signals = [calculate_signal_strength(adj_list, [path], xi, yi) for path in paths]

    # 计算一对目标节点符合条件的路径的信息熵并累加
    total_entropy = sum(calculate_entropy_per_path(signal) for signal in path_signals)

    return total_entropy



if __name__ == '__main__':

    # 初始化图和邻接列表
    edges = pd.read_csv(r'DataSet\dolphins_delete_target.csv', header=None, sep='\t').values
    adj_list = build_adjacency_list(edges)
    G=create_graph_from_adjacency_list(adj_list)
    # 假设 deleted_edges 包含所有目标边对
    deleted_edges = read_edges_from_csv( 'DataSet/target_edges.csv' )

    All_Entropy = 0

    for xi, yi in deleted_edges:
        path_file = f"ComPath/{xi},{yi}.csv"
        paths = read_paths_from_csv(path_file)
        total_signal = calculate_signal_strength(adj_list, paths, xi, yi)
        total_entropy = calculate_total_entropy(adj_list, paths, xi, yi)

        All_Entropy +=total_entropy

        print(f"Edge {xi}-{yi}: Total signal strength = {total_signal}, Total entropy = {total_entropy}")

    print(f"ALL ENTROPY: {All_Entropy}")

"""
def calculate_signal_strength_per_path(adj_list , path) :
    signal = 1.0  # 从源节点出发，信号量为1
    for i , node in enumerate ( path[1 :-1] , 1 ) :  # 排除目标节点
        degree = len ( adj_list[node] )
        signal /= degree  # 根据节点度数分裂信号
    return signal

def calculate_entropy(adj_list , paths , source_node , target_node) :
    path_signals = calculate_signal_strength ( adj_list , paths , source_node , target_node )

    # 计算每条路径的信息熵
    entropies = [-signal * math.log ( signal , 2 ) for signal in path_signals if signal > 0]

    # 计算总信息熵
    total_entropy = sum ( entropies )
    return total_entropy"""


"""def calculate_signal(adj_list, paths):
    # 初始化所有节点的信号量为0
    node_signal = {node: 0 for node in adj_list}
    node_signal[source_node] = 1  # 源节点信号量设置为1

    # 按路径长度从小到大排序
    paths.sort(key=len)

    # 逐条路径计算信号量
    for path in paths:
        signal = node_signal[path[0]]  # 获取路径起始节点的信号量
        for node in path[1:]:  # 从路径的第二个节点开始计算
            signal /= len(adj_list[node])  # 按节点度数衰减信号量
            node_signal[node] += signal  # 累加信号量到当前节点

    # 最终目标节点的信号量即为所有路径上信号量的总和
    final_signal = node_signal[target_node]
    return final_signal


# 计算信号量总和
total_signal = calculate_signal(adj_list, paths)
print(f"Total signal strength at node {target_node} is: {total_signal}")"""
