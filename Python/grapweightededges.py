import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import heapq

class Graph:
    def __init__(self, data={}):
        self.data = data

    def add_node(self, value):
        if value not in self.data.keys():
            self.data[value] = []

    def add_edge(self, node1, node2, weight = 0):
       if node1 and node2 in self.data.keys():
           self.data[node1].append((node2, weight))
           self.data[node1].sort()
           self.data[node2].append((node1, weight))
           self.data[node2].sort()

    def get_data(self):
        return self.data

    def get_nodes(self):
        return list(self.data.keys())


    def get_neighbors(self, node):
        return self.data.get(node, {})


    def get_edges(self):
        edges = []
        for node1 in self.data.keys():
            for node2 in self.data[node1]:
                if (node2, node1) not in edges:
                    edges.append((node2, node1))
        return edges

    def remove_edge(self, node1, node2):
        self.data[node1] = [(n, w) for n, w in self.data[node1] if n != node2]
        self.data[node2] = [(n, w) for n, w in self.data[node2] if n != node1]
        if node1 in self.data[node2] and node2 in self.data[node1]:
            self.data[node1].remove(node2)
            self.data[node2].remove(node1)


    def remove_node(self, node):
        if node in self.data.keys():
            for current in self.data.keys():
                if node in self.data[current]:
                    self.data[current].remove(node)
            del self.data[node]

    def adjacency_matrix(self):
        nodes = self.get_nodes()
        size = len(nodes)
        index = {node: i for i, node in enumerate(nodes)}

        matrix = [[0] * size for _ in range(size)]

        for node in nodes:
            for neighbor, weight in self.data[node]:
                i = index[node]
                j = index[neighbor]
                matrix[i][j] = weight
        print(" ", end='')

        for node in nodes:
            print(f"{node}", end=' ')
        print()

        for i, row in enumerate(matrix):
            print(f"nodes{i}", end=' ')

            for val in row:
                print(f"{val}", end=' ')

                print()

def dfs(g, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for neighbor in g.get_neighbors(start):
        if neighbor not in visited:
            dfs(g, neighbor, visited)
    return visited

def bfs(g, start):
    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        for neighbor in g.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited

def dijkstra(graph, start):
    nodes = graph.get_nodes()

    cost = {node: float("inf") for node in nodes}
    prev = {node: None for node in nodes}
    visited = set()

    cost[start] = 0
    pq = [(0, start)]
    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue

        visited.add(current_node)
        for neighbor, weight in graph.get_neighbors(current_node):
            if neighbor in visited:
                continue

            dist = current_dist + weight

            if dist < cost[neighbor]:
                cost[neighbor] = dist
                prev[neighbor] = current_node
                heapq.heappush(pq, (dist, neighbor))

    return {'cost': cost, 'prev': prev, 'visited': visited}

def get_path(data, target):
    path = []
    current = target

    while current is not None:
        path.append(current)
        current = data['prev'][current]
    path.reverse()
    return path


def main():
   g = nx.Graph()
   g.add_edge("g", "f", weight=3.5)
   g.add_edge("b", "g", weight=4)
   g.add_edge("b", "f", weight=8)
   g.add_edge("b", "a", weight=5)
   g.add_edge("c", "a", weight=2)
   g.add_edge("e", "a", weight=10)
   g.add_edge("d", "c", weight=12)
   g.add_edge("d", "e", weight=6)

   elarge = [(node1, node2) for (node1, node2, weight) in g.edges(data=True) if weight["weight"] > 1]
   esmall = [(node1, node2) for (node1, node2, weight) in g.edges(data=True) if weight["weight"] <= 1]

   pos = nx.spring_layout(g, seed=8)

   nx.draw_networkx_nodes(g, pos, node_size=700, node_color='blue')

   nx.draw_networkx_edges(g, pos, edgelist=elarge, width=2.5, edge_color='red')
   nx.draw_networkx_edges(g, pos, edgelist=esmall, width=2.5, edge_color='gray', style='dashed')

   nx.draw_networkx_labels(g, pos, font_size=12, font_family="sans-serif")

   edge_labels = nx.get_edge_attributes(g, "weight")
   nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)


   plt.axis("off")
   plt.title("Graph Visualization with Edge Weights")
   plt.show()


main()