import matplotlib.pyplot as plt
import networkx as nx

# Create the Karate Club graph using NetworkX
G = nx.karate_club_graph()

# Define colors and outline each faction
node_colors = []
for node in G.nodes(data=True):
    if node[1]['club'] == 'Mr. Hi':
        node_colors.append('salmon')  # Color for Mr. Hi's faction
    else:
        node_colors.append('white')  # Color for John's faction

# Adjust labels to display 1-34 instead of 0-33
labels = {node: node + 1 for node in G.nodes()}

# Draw the graph with colored nodes and outlines
plt.figure(figsize=(10, 8))

# POsition nodes using a layout for better visualization
pos = nx.kamada_kawai_layout(G)

# Draw nodes with black outlines
nx.draw_networkx_nodes(
    G, pos, node_color=node_colors, node_size=500,
    edgecolors='black', linewidths=1
)

# Draw edges and labels
nx.draw_networkx_edges(G, pos, edge_color='gray')
nx.draw_networkx_labels(G, pos, labels=labels)

# Add title and display the plot
plt.title("Karate Club Graph Colored by Faction")
plt.axis('off')
plt.show()