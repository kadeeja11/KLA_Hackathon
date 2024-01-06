import json
import networkx as nx

def recommend_path(n_neighbourhoods, start, distances):
    G = nx.Graph()

    # Flatten distances dictionary for better readability
    flat_distances = distances["neighbourhoods"]

    # Add edges based on neighborhood distances
    G.add_weighted_edges_from((i, j, flat_distances[f"n{i}"]["distances"][j])
                              for i in range(n_neighbourhoods) for j in range(n_neighbourhoods) if i != j)

    # Find the shortest path that covers all neighborhoods
    path = nx.approximation.traveling_salesman_problem(G, cycle=True, weight='weight')

    # Prepare JSON output
    output = {"v0": {"path": [f"r0"] + [f"n{node}" for node in path[:-1]] + [f"r0"]}}

    return output

if __name__ == "__main__":
    with open("level0.json", "r") as file:
        input_data = json.load(file)

    n_neighbourhoods = input_data["n_neighbourhoods"]
    start_location = 0  # Assuming the restaurant is at location 0

    distances = input_data["restaurants"]["r0"]

    output = recommend_path(n_neighbourhoods, start_location, input_data)

    # Print the JSON output with indentation for better readability
    print(json.dumps(output, indent=2))
