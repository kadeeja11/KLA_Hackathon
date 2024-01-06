import json
import networkx as nx

def recommend_delivery_path(n_neighbourhoods, vehicles, distances, order_quantities):
    G = nx.Graph()

    # Convert integer indices to strings for node labels
    for i, data_i in distances.items():
        i = str(i)
        for j, distance in enumerate(data_i["distances"]):
            G.add_edge(i, f"n{j}", weight=distance)

    # Add edges based on restaurant distances
    restaurant_distances = distances.get("r0", {}).get("neighbourhood_distance", [0] * n_neighbourhoods)
    for i, distance in enumerate(restaurant_distances):
        G.add_edge(f"n{i}", "r0", weight=distance)

    paths = {}

    # Iterate over each vehicle
    for vehicle_name, vehicle_data in vehicles.items():
        path_count = 0
        capacity = vehicle_data["capacity"]
        current_node = vehicle_data["start_point"]
        current_path = [current_node]

        remaining_nodes = set(G.nodes())
        remaining_nodes.remove(current_node)

        while remaining_nodes:
            nearest_neighbor = min(remaining_nodes, key=lambda node: G[current_node][node]['weight'])

            if nearest_neighbor == "r0":
                current_path.append(nearest_neighbor)
                paths.setdefault(vehicle_name, {})[f"path{path_count + 1}"] = current_path.copy()
                path_count += 1
                current_node = vehicle_data["start_point"]
                current_path = [current_node]
                capacity = vehicle_data["capacity"]
            else:
                nearest_neighbor_str = nearest_neighbor[1:]
                if order_quantities[nearest_neighbor_str] <= capacity:
                    current_path.append(nearest_neighbor)
                    capacity -= order_quantities[nearest_neighbor_str]
                    remaining_nodes.remove(nearest_neighbor)
                    current_node = nearest_neighbor
                else:
                    current_path.append(vehicle_data["start_point"])
                    paths.setdefault(vehicle_name, {})[f"path{path_count + 1}"] = current_path.copy()
                    path_count += 1
                    current_node = vehicle_data["start_point"]
                    current_path = [current_node]
                    capacity = vehicle_data["capacity"]

        current_path.append(vehicle_data["start_point"])
        paths.setdefault(vehicle_name, {})[f"path{path_count + 1}"] = current_path.copy()

    # Prepare the output JSON
    output = json.dumps(paths, indent=2)

    return output

if __name__ == "__main__":
    with open("level2a.json", "r") as file:
        input_data = json.load(file)

    n_neighbourhoods = input_data["n_neighbourhoods"]
    vehicles = input_data["vehicles"]
    distances = input_data["neighbourhoods"]

    # Update the order_quantities dictionary to include the restaurant with capacity 0
    order_quantities = {key[1:]: data["order_quantity"] for key, data in distances.items()}
    order_quantities["0"] = 0  # Assuming the restaurant's order quantity is 0

    output = recommend_delivery_path(n_neighbourhoods, vehicles, distances, order_quantities)

    # Print the JSON output with indentation for better readability
    print(output)
