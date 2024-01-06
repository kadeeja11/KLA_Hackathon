import json
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model(n_neighbourhoods, start, distances, order_quantities, capacity):
    data = {}
    data['n_neighbourhoods'] = n_neighbourhoods
    data['num_vehicles'] = 1
    data['depot'] = start
    data['distances'] = distances
    data['order_quantities'] = order_quantities
    data['vehicle_capacity'] = capacity
    return data

def recommend_delivery_path(data):
    manager = pywrapcp.RoutingIndexManager(data['n_neighbourhoods'], data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    # Define distance callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distances'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Define demand callback
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['order_quantities'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(demand_callback_index, 0, [data['vehicle_capacity']], True, 'Capacity')

    # Set 10 seconds as the maximum time allowed per each vehicle in a route
    routing.AddDimension(transit_callback_index, 0, 10, True, 'Time')

    # Solve the problem
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    solution = routing.SolveWithParameters(search_parameters)

    # Retrieve the solution
    output = {'v0': {'path1': []}}
    if solution:
        index = routing.Start(0)
        while not routing.IsEnd(index):
            output['v0']['path1'].append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        output['v0']['path1'].append(manager.IndexToNode(index))

    return output

if __name__ == '__main__':
    with open('C:/KLA_MOCK_HACKTHON/Student Handout/Input data/level1a.json', 'r') as file:
        input_data = json.load(file)

    n_neighbourhoods = input_data['n_neighbourhoods']
    start_location = input_data['vehicles']['v0']['start_point']
    distances = input_data['neighbourhoods']

    order_quantities = {key[1:]: data['order_quantity'] for key, data in distances.items()}
    order_quantities['0'] = 0

    capacity = input_data['vehicles']['v0']['capacity']

    data_model = create_data_model(n_neighbourhoods, start_location, distances, order_quantities, capacity)
    output = recommend_delivery_path(data_model)

    print(json.dumps(output, indent=2))
