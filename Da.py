import sys
import random
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QRadioButton, QLineEdit, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from time import time

# Kruskal's Algorithm Classes
class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.edges = []

    def add_edge(self, src, dest, weight):
        self.edges.append(Edge(src, dest, weight))

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        root_x = self.find(parent, x)
        root_y = self.find(parent, y)
        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_y] = root_x
            rank[root_x] += 1

    def kruskal_mst(self):
        result = []
        self.edges = sorted(self.edges, key=lambda edge: edge.weight)
        parent, rank = list(range(self.V)), [0] * self.V
        
        for edge in self.edges:
            x, y = self.find(parent, edge.src), self.find(parent, edge.dest)
            if x != y:
                result.append((edge.src, edge.dest, edge.weight))
                self.union(parent, rank, x, y)
        
        return result

# Prim's Algorithm Classes
class PrimGraph:
    def __init__(self, vertices):
        self.V = vertices
        self.adj_list = {i: [] for i in range(vertices)}

    def add_edge(self, src, dest, weight):
        self.adj_list[src].append((weight, dest))
        self.adj_list[dest].append((weight, src))

    def prim_mst(self):
        visited = [False] * self.V
        min_heap = [(0, 0)]  # (weight, vertex)
        mst_edges = []
        
        while min_heap and len(mst_edges) < self.V - 1:
            weight, u = heapq.heappop(min_heap)
            if visited[u]:
                continue
            visited[u] = True
            for edge_weight, v in self.adj_list[u]:
                if not visited[v]:
                    heapq.heappush(min_heap, (edge_weight, v))
                    mst_edges.append((u, v, edge_weight))
        
        return mst_edges

# PyQt5 GUI Application
class MSTApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Minimum Spanning Tree Comparison")
        layout = QVBoxLayout()

        # Algorithm Selection
        layout.addWidget(QLabel("Choose Algorithm:"))
        self.kruskal_radio = QRadioButton("Kruskal")
        self.kruskal_radio.setChecked(True)
        self.prim_radio = QRadioButton("Prim")
        layout.addWidget(self.kruskal_radio)
        layout.addWidget(self.prim_radio)
        
        # Input for Graph Size
        layout.addWidget(QLabel("Number of Nodes:"))
        self.nodes_entry = QLineEdit()
        layout.addWidget(self.nodes_entry)
        
        # Run and Compare buttons
        self.run_button = QPushButton("Run Algorithm")
        self.run_button.clicked.connect(self.run_algorithm)
        layout.addWidget(self.run_button)

        self.compare_button = QPushButton("Compare Algorithms")
        self.compare_button.clicked.connect(self.compare_algorithms)
        layout.addWidget(self.compare_button)

        # Result Display
        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        # Graph Visualization
        self.figure = plt.figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def generate_random_edges(self, num_nodes):
        return [(random.randint(0, num_nodes - 1), random.randint(0, num_nodes - 1), random.randint(1, 100)) for _ in range(num_nodes * 2)]

    def run_algorithm(self):
        num_nodes = int(self.nodes_entry.text())
        edges = self.generate_random_edges(num_nodes)
        start_time = time()

        if self.kruskal_radio.isChecked():
            graph = Graph(num_nodes)
            for src, dest, weight in edges:
                graph.add_edge(src, dest, weight)
            result = graph.kruskal_mst()
            title = "Kruskal's MST"
        else:
            graph = PrimGraph(num_nodes)
            for src, dest, weight in edges:
                graph.add_edge(src, dest, weight)
            result = graph.prim_mst()
            title = "Prim's MST"

        end_time = time()
        runtime = end_time - start_time
        self.result_label.setText(f"Runtime: {runtime:.4f} seconds")
        
        # Visualize MST
        self.visualize_mst(result, title)

    def compare_algorithms(self):
        num_nodes = int(self.nodes_entry.text())
        edges = self.generate_random_edges(num_nodes)

        # Kruskal's algorithm
        kruskal_start = time()
        kruskal_graph = Graph(num_nodes)
        for src, dest, weight in edges:
            kruskal_graph.add_edge(src, dest, weight)
        kruskal_result = kruskal_graph.kruskal_mst()
        kruskal_end = time()
        kruskal_runtime = kruskal_end - kruskal_start

        # Prim's algorithm
        prim_start = time()
        prim_graph = PrimGraph(num_nodes)
        for src, dest, weight in edges:
            prim_graph.add_edge(src, dest, weight)
        prim_result = prim_graph.prim_mst()
        prim_end = time()
        prim_runtime = prim_end - prim_start

        # Display results and visualize MSTs for both algorithms
        self.result_label.setText(f"Kruskal: {kruskal_runtime:.4f} s | Prim: {prim_runtime:.4f} s")
        self.visualize_mst(kruskal_result, title="Kruskal's MST")
        self.visualize_mst(prim_result, title="Prim's MST")

    def visualize_mst(self, mst_edges, title="Minimum Spanning Tree"):
        G = nx.Graph()
        for u, v, weight in mst_edges:
            G.add_edge(u, v, weight=weight)

        pos = nx.spring_layout(G, k=0.5, iterations=50)  # Adjusted k-value for spacing
        weights = nx.get_edge_attributes(G, 'weight')

        # Clear the previous figure for a fresh draw
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        nx.draw(G, pos, ax=ax, with_labels=True, node_color='skyblue', edge_color='black', node_size=400, font_size=8)
        nx.draw_networkx_edges(G, pos, ax=ax, width=1.5, edge_color="orange")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=weights, ax=ax, font_size=7, font_color="blue")
        ax.set_title(title)
        self.canvas.draw()

# Running the Application
app = QtWidgets.QApplication(sys.argv)
window = MSTApp()
window.show()
sys.exit(app.exec_())
