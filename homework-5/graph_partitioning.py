import matplotlib.pyplot as plt
import networkx as nx
import os

# Create the Karate Club graph using NetworkX
G = nx.karate_club_graph()

def save_graph_snapshot(graph, pos, title, output_path, node_colors, node_size=500):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph)

    # Draw nodes with predefined colors and black outlines
    nx.draw_networkx_nodes(
        graph, pos, node_color=node_colors,
        node_size=node_size, edgecolors='black', linewidths=1
    )

    # Draw edges and labels
    nx.draw_networkx_edges(graph, pos, edge_color='gray')
    nx.draw_networkx_labels(graph, pos)

    # Save the figure as the initial state
    plt.title(title)
    plt.axis('off')
    plt.savefig(os.path.join(output_path))
    plt.close()

# Define colors and outline each faction
def get_node_colors(graph):
    node_colors = []
    for node in graph.nodes(data=True):
        if node[1]['club'] == 'Mr. Hi':
            node_colors.append('salmon')  # Color for Mr. Hi's faction
        else:
            node_colors.append('white')  # Color for John's faction
    return node_colors

def girvan_newman_visualization(graph):
    # Make a copy of the graph to avoid modifying the original
    working_graph = graph.copy()
    iteration = 1

    # Create a directory for saving images if it doesn't exist
    output_dir = "homework-5/iterations"
    os.makedirs(output_dir, exist_ok=True)

    # Initial position and node colors
    pos = nx.spring_layout(graph)
    node_colors = get_node_colors(graph)

    # Save the initial graph
    save_graph_snapshot(
        graph, pos, "Initial Karate Club Graph",
        os.path.join("homework-5", "initial_karate_club_graph.png"),
        node_colors
    )

    while nx.number_connected_components(working_graph) == 1:
        # Calculate edge betweenness centrality and remove the highest edge
        edge_betweenness = nx.edge_betweenness_centrality(working_graph)
        edge_to_remove = max(edge_betweenness, key=edge_betweenness.get)
        working_graph.remove_edge(*edge_to_remove)

        if nx.number_connected_components(working_graph) > 1:
            break

        # Save snapshot for each iteration
        save_graph_snapshot(
            working_graph, pos, 
            f"Iteration {iteration} of Girvan-Newman Algorithm",
            os.path.join(output_dir, f"girvan_newman_iteration_{iteration}.png"),
            node_colors
        )

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