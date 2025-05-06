import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),
    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

pos = {
    "Термінал 1": (-1, 0),  "Термінал 2": (3, 0),
    "Склад 1": (0, 1.5),    "Склад 2": (2, 1.5),
    "Склад 3": (0, -1.5),   "Склад 4": (2, -1.5),
    "Магазин 1": (-2, 3),   "Магазин 2": (-1, 3),
    "Магазин 3": (0, 3),    "Магазин 4": (1, 3),
    "Магазин 5": (2, 3),    "Магазин 6": (3, 3),
    "Магазин 7": (-2, -3),  "Магазин 8": (-1, -3),
    "Магазин 9": (0, -3),   "Магазин 10": (1, -3),
    "Магазин 11": (2, -3),  "Магазин 12": (3, -3),
    "Магазин 13": (4, -3),  "Магазин 14": (5, -3),
}

super_source = "Джерело"
super_sink = "Сток"
terminals = ["Термінал 1", "Термінал 2"]
warehouses = [f"Склад {i}" for i in range(1, 5)]
stores = [f"Магазин {i}" for i in range(1, 15)]


def initialize_graph():
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    for t in terminals:
        G.add_edge(super_source, t, weight=float('inf'))
    for node in list(G.nodes):
        if node.startswith("Магазин"):
            G.add_edge(node, super_sink, weight=float('inf'))
    return G


def build_capacity_matrix(G):
    nodes = list(G.nodes)
    node_indices = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)
    capacity_matrix = [[0] * n for _ in range(n)]
    for u, v, data in G.edges(data=True):
        i, j = node_indices[u], node_indices[v]
        capacity_matrix[i][j] = data["weight"]
    return nodes, node_indices, capacity_matrix


def bfs(capacity, flow, source, sink, parent):
    visited = [False] * len(capacity)
    queue = deque([source])
    visited[source] = True
    while queue:
        u = queue.popleft()
        for v in range(len(capacity)):
            if not visited[v] and capacity[u][v] - flow[u][v] > 0:
                parent[v] = u
                visited[v] = True
                if v == sink:
                    return True
                queue.append(v)
    return False


def edmonds_karp(capacity, source, sink):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    parent = [-1] * n
    max_flow = 0
    while bfs(capacity, flow, source, sink, parent):
        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(
                path_flow, capacity[parent[s]][s] - flow[parent[s]][s])
            s = parent[s]
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = parent[v]
        max_flow += path_flow
    return max_flow, flow


def print_terminal_flows(flow, node_indices):
    print("Таблиця фактичних потоків (термінал - магазин):")
    for term in terminals:
        term_idx = node_indices[term]
        for store_num in range(1, 15):
            store = f"Магазин {store_num}"
            store_idx = node_indices[store]
            total_flow = 0
            for warehouse in warehouses:
                w_idx = node_indices[warehouse]
                if flow[w_idx][store_idx] > 0 and flow[term_idx][w_idx] > 0:
                    total_flow += min(flow[w_idx][store_idx],
                                      flow[term_idx][w_idx])
            if total_flow > 0:
                print(f"{term} - {store}: {total_flow} од.")


def draw_graph(G):
    plt.figure(figsize=(15, 10))
    visible_nodes = [node for node in G.nodes if node in pos]
    nx.draw(
        G.subgraph(visible_nodes), pos,
        with_labels=True, node_size=2000, node_color="skyblue",
        font_size=12, arrows=True
    )
    visible_edges = [(u, v) for u, v in G.edges() if u in pos and v in pos]
    visible_labels = {(u, v): G[u][v]["weight"] for u, v in visible_edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=visible_labels)
    plt.title("Логістична мережа (граф потоків)")
    plt.show()


def main():
    G = initialize_graph()
    node, node_indices, capacity = build_capacity_matrix(G)
    source = node_indices[super_source]
    sink = node_indices[super_sink]
    max_flow, flow = edmonds_karp(capacity, source, sink)
    print(f"Максимальний потік у логістичній мережі: {max_flow}")
    print_terminal_flows(flow, node_indices)
    draw_graph(G)


if __name__ == "__main__":
    main()
