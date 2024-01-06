import json
import networkx as nx

def recommend_delivery_path(n_neighbourhoods, start, distances, order_quantities, capacity):
    G = nx.Graph()

    # Convert integer indices to strings for node labels
    start = str(start)
    for i, data_i in distances.items():
        i = str(i)
        for j, distance in enumerate(data_i["distances"]):
            G.add_edge(i, f"n{j}", weight=distance)

    # Add edges based on restaurant distances
    restaurant_distances = distances.get("r0", {}).get("neighbourhood_distance", [0] * n_neighbourhoods)
    for i, distance in enumerate(restaurant_distances):
        G.add_edge(f"n{i}", "r0", weight=distance)

    paths = {}
    path_count = 0

    # Nearest Neighbor Algorithm
    remaining_nodes = set(G.nodes())
    remaining_nodes.remove(start)

    current_node = start
    current_path = [current_node]

    while remaining_nodes:
        nearest_neighbor = min(remaining_nodes, key=lambda node: G[current_node][node]['weight'])

        # Handle the restaurant node separately
        if nearest_neighbor == "r0":
            current_path.append(nearest_neighbor)
            paths[f"path{path_count + 1}"] = current_path
            path_count += 1
            current_node = start
            current_path = [current_node]
            capacity = input_data["vehicles"]["v0"]["capacity"]
        else:
            # Remove 'n' prefix and keep the numeric part as a string
            nearest_neighbor_str = nearest_neighbor[1:]

            if order_quantities[nearest_neighbor_str] <= capacity:
                current_path.append(nearest_neighbor)
                capacity -= order_quantities[nearest_neighbor_str]
                remaining_nodes.remove(nearest_neighbor)
                current_node = nearest_neighbor
            else:
                current_path.append("r0")
                paths[f"path{path_count + 1}"] = current_path
                path_count += 1
                current_node = start
                current_path = [current_node]
                capacity = input_data["vehicles"]["v0"]["capacity"]

    current_path.append("r0")
    paths[f"path{path_count + 1}"] = current_path

    # Prepare the output JSON
    output = {"v0": paths}

    return output

if __name__ == "__main__":
    with open("C:/KLA_MOCK_HACKTHON/Student Handout/Input data/level1a.json", "r") as file:
        input_data = json.load(file)

    n_neighbourhoods = input_data["n_neighbourhoods"]
    start_location = input_data["vehicles"]["v0"]["start_point"]

    distances = input_data["neighbourhoods"]
    
    # Update the order_quantities dictionary to include the restaurant with capacity 0
    order_quantities = {key[1:]: data["order_quantity"] for key, data in distances.items()}
    order_quantities["0"] = 0  # Assuming the restaurant's order quantity is 0

    capacity = input_data["vehicles"]["v0"]["capacity"]

    output = recommend_delivery_path(n_neighbourhoods, start_location, distances, order_quantities, capacity)

    # Print the JSON output with indentation for better readability
    print(json.dumps(output, indent=2))
