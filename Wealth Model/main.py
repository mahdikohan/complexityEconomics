import networkx as nx
import random
import matplotlib.pyplot as plt

# Function to perform trades
def trade(graph, steps):
    for _ in range(steps):
        edge = random.choice(list(graph.edges))
        if random.choice([True, False]):
            node1, node2 = edge
        else:
            node2, node1 = edge
        if graph.nodes[node1]['wallet'] > 0:
            graph.nodes[node1]['wallet'] -= 1
            graph.nodes[node2]['wallet'] += 1

# Initialize an empty list to store the graphs
graphs = []

# Create 10 graphs
for i in range(10):
    graph = nx.Graph()
    for j in range(10):
        graph.add_node(j, wallet=1)
    for node1 in graph.nodes:
        for node2 in graph.nodes:
            if node1 != node2:
                graph.add_edge(node1, node2)
    graphs.append(graph)

# Perform trades and collect final 'wallet' values
wallet_values = []
for graph in graphs:
    trade(graph, 10)  # Changed the number of steps to 10
    for node in graph.nodes:
        wallet_values.append(graph.nodes[node]['wallet'])

# Plot a histogram of 'wallet' values
plt.figure(figsize=(10, 5))
plt.hist(wallet_values, bins=range(min(wallet_values), max(wallet_values) + 1))
plt.xlabel('Wallet Value')
plt.ylabel('Frequency')
plt.title('Histogram of Wallet Values After Trades')
plt.show()

# Plot the graphs with node sizes proportional to 'wallet' values
for i, graph in enumerate(graphs, start=1):
    plt.figure(figsize=(5, 5))
    node_sizes = [graph.nodes[node]['wallet']*500+100 for node in graph.nodes]
    nx.draw(graph, with_labels=True, node_size=node_sizes)
    plt.title(f'Graph {i} After Trades')
    plt.show()
