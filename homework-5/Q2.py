import matplotlib.pyplot as plt
import networkx as nx
import os

# Create the Karate Club graph using NetworkX
G = nx.karate_club_graph()

# Define colors and outline each faction
def get_node_colors(graph):
    node_colors = []
    for node in graph.nodes(data=True):
        if node[1]['club'] == 'Mr. Hi':
            node_colors.append('salmon')  # Color for Mr. Hi's faction
        else:
            node_colors.append('white')  # Color for John's faction
    return node_colors

# Adjust labels to display 1-34 instead of 0-33
labels = {node: node + 1 for node in G.nodes()}

def girvan_newman_visualization(graph):
    # Make a copy of the graph to avoid modifying the original
    working_graph = graph.copy()
    iteration = 1

    # Create a directory for saving images if it doesn't exist
    output_dir = "iterations"
    os.makedirs(output_dir, exist_ok=True)

    while nx.number_connected_components(working_graph) == 1:
        # Calculate edge betweenness centrality
        edge_betweenness = nx.edge_betweenness_centrality(working_graph)

        # Find the edge with the highest centrality and remove it
        edge_to_remove = max(edge_betweenness, key=edge_betweenness.get)
        working_graph.remove_edge(*edge_to_remove)

        # Draw the graph at each iteration
        plt.figure(figsize=(10, 8))
        pos = nx.kamada_kawai_layout(working_graph)

        # Draw nodes with predefined colors and black outlines
        nx.draw_networkx_nodes(
            working_graph, pos, node_color=get_node_colors(graph), 
            node_size=500, edgecolors='black', linewidths=1
        )

        # Draw edges and labels
        nx.draw_networkx_edges(working_graph, pos, edge_color='gray')
        nx.draw_networkx_labels(working_graph, pos, labels=labels)

        # Title for each iteration
        plt.title(f"Iteration {iteration} of Girvan-Newman Algorithm")
        plt.axis('off')

        # Save the figure as an image file
        plt.savefig(os.path.join(output_dir, f"girvan_newman_iteration_{iteration}.png"))
        # plt.show()

        # Increment iteration counter
        iteration += 1

    # Return the final split components for analysis
    components = list(nx.connected_components(working_graph))

    # Print the number of iterations
    print(f"Number of iterations: {iteration}")

    return components

# Run the Girvan-Newman visualization and save images
components = girvan_newman_visualization(G)
print("Final components:", components)