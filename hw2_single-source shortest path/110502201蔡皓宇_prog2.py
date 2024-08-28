import math
import copy
import random

positive_inf = math.inf
negative_inf = -math.inf

# weight_table
def construct_weight_table(dataset, num_vertex, num_edge):
    weight_table = [[positive_inf] * num_vertex for _ in range(num_vertex)]
    for i in range(num_vertex):
        weight_table[i][i] = 0
    for edge in dataset:
        u, v, w = edge[0], edge[1], edge[2]
        weight_table[u][v] = w
    return weight_table

# determine whether the graph is DAG or not
def check_cycle(dataset, num_vertex, num_edge, source):
    dataset_modified = copy.deepcopy(dataset)
    for i in range(num_edge):
        dataset_modified[i][2] = -1 * random.randint(1, 10)
    # detect whether there's a cycle(whether p-cycle or n-cycle) in the graph
    has_negative_cycle, dist = bellman_ford(dataset_modified, num_vertex, num_edge, source)
    if has_negative_cycle: return True
    else: return False

# Dijkstra
def dijkstra(dataset, num_vertex, num_edge, source):
    W = construct_weight_table(dataset, num_vertex, num_edge)
    dist = [positive_inf] * num_vertex
    dist[source] = 0
    checked = [False] * num_vertex
    for _ in range(num_vertex):
        minimum, min_index = positive_inf, -1
        # choose the min vertex distance
        for i in range(num_vertex):
            if dist[i] < minimum and (not checked[i]):
                minimum, min_index = dist[i], i
        # update all Adj[k] distance
        for k in range(num_vertex):
            if dist[k] > dist[min_index] + W[min_index][k]:
                dist[k] = dist[min_index] + W[min_index][k]
        checked[min_index] = True
    return dist

# Bellman-Ford
def bellman_ford(dataset, num_vertex, num_edge, source):
    W = construct_weight_table(dataset, num_vertex, num_edge)
    dist = [positive_inf] * num_vertex
    dist[source] = 0
    for _ in range(num_vertex-1):
        for edge in dataset:
            u, v, w = edge[0], edge[1], edge[2]
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w  
    # check existence of negative cycle       
    for edge in dataset:
        u, v, w = edge[0], edge[1], edge[2]
        if dist[v] > dist[u] + w:
            return True, dist # T: there is a negative-weight-cycle
    return False, dist # F: there is no negative-weight-cycle

def print_ans(dist_ans):
    for i in range(len(dist_ans)):
        if i == 0:
            continue
        print(f'0 {i} {dist_ans[i]}')

# main function
def main():
    global has_negative_edge, has_negative_cycle, has_whatever_cycle
    has_negative_edge, has_negative_cycle, has_whatever_cycle = False, False, False
    dataset = []
    dist_ans = []
    with open('input.txt', 'r') as f:
        for line in f:
            dataset.append(list(map(int, line.strip().split())))
    num_vertex, num_edge, source = dataset[0][0], dataset[0][1], 0
    dataset = dataset[1:]

    # check negative edge
    for i in range(num_edge):
        if dataset[i][2] < 0:
            has_negative_edge = True
            break
    
    has_whatever_cycle = check_cycle(dataset, num_vertex, num_edge, source)
    if not has_whatever_cycle:
        print("A directed acyclic graph")
        
    if has_negative_edge:
        has_negative_cycle, dist_ans = bellman_ford(dataset, num_vertex, num_edge, source)
        if has_negative_cycle:
            print("A graph with negative weight cycles")
            print("No shortest paths can be found.")
        else:
            print("A graph with negative weight edges but no negative weight cycles")
            print("All shortest paths from source vertex 0 is:")
            print_ans(dist_ans)
    else:
        dist_ans = dijkstra(dataset, num_vertex, num_edge, source)
        has_negative_cycle = False
        print("A graph with no negative weight edges")
        print("All shortest paths from source vertex 0 is:")
        print_ans(dist_ans)
      

if __name__ == '__main__':
    main()
