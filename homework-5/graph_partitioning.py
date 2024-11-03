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

# Function to save the initial graph before iterations
def save_initial_graph(graph):
    plt.figure(figsize=(10, 8))
    pos = nx.kamada_kawai_layout(graph)

    # Draw nodes with predefined colors and black outlines
    nx.draw_networkx_nodes(
        graph, pos, node_color=get_node_colors(graph),
        node_size=500, edgecolors='black', linewidths=1
    )

    # Draw edges and labels
    nx.draw_networkx_edges(graph, pos, edge_color='gray')
    nx.draw_networkx_labels(graph, pos)

    # Save the figure as the initial state
    plt.title("Initial Karate Club Graph")
    plt.axis('off')
    plt.savefig(os.path.join("homework-5", "intial_karate_club_graph.png"))
    plt.close()

def girvan_newman_visualization(graph):
    # Save the initial graph
    save_initial_graph(graph)
    
    # Make a copy of the graph to avoid modifying the original
    working_graph = graph.copy()
    iteration = 1

    # Create a directory for saving images if it doesn't exist
    output_dir = "homework-5/iterations"
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
        nx.draw_networkx_labels(working_graph, pos)

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
    print(f"Number of iterations: {iteration}\n")

    return components

# Run the Girvan-Newman visualization and save images
components = girvan_newman_visualization(G)
# print("Final components:", components)

# Get the actual factions
mr_hi_faction = {node for node, attr in G.nodes(data=True) if attr['club'] == 'Mr. Hi'}
john_faction = {node for node, attr in G.nodes(data=True) if attr['club']== "Officer"}
actual_split = [mr_hi_faction, john_faction]

print("Actual split factions:")
print("Mr. Hi's faction:", mr_hi_faction)
print("John's faction:", john_faction)

# Compare Girvan-Newman components to actual factions
matching_results = []
for component in components:
    if component == mr_hi_faction or component == john_faction:
        matching_results.append("Yes, matched")
    else:
        matching_results.append("No, not matched")

print("\nComparison of Girvan-Newman results with actual split:")
for i, component in enumerate(components, 1):
    print(f"Component {i}: {component}")
    print(f"Matches actual factions? {matching_results[i-1]}")