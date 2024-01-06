#include <iostream>
#include <vector>
#include <unordered_map>
#include <stack>
#include <fstream>
#include <nlohmann/json.hpp>

using namespace std;
using json = nlohmann::json;

class Graph {
public:
    Graph(int vertices) : vertices(vertices), graph(vertices) {}

    void addEdge(int u, int v) {
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    vector<int> findPath(int start) {
        vector<int> path;
        vector<bool> visited(vertices, false);
        stack<int> s;

        s.push(start);
        visited[start] = true;

        while (!s.empty()) {
            int node = s.top();
            s.pop();
            path.push_back(node);

            for (int neighbor : graph[node]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    s.push(neighbor);
                }
            }
        }

        return path;
    }

private:
    int vertices;
    vector<vector<int>> graph;
};

vector<int> recommendPath(int nNeighbourhoods, int start, unordered_map<string, vector<int>>& distances) {
    Graph graph(nNeighbourhoods);

    // Add edges based on neighborhood distances
    for (int i = 0; i < nNeighbourhoods; ++i) {
        for (int j = 0; j < nNeighbourhoods; ++j) {
            if (i != j) {
                graph.addEdge(i, j);
            }
        }
    }

    // Add edges based on restaurant distances
    for (int i = 0; i < nNeighbourhoods; ++i) {
        graph.addEdge(i, nNeighbourhoods);
    }

    // Find the path using DFS
    return graph.findPath(start);
}

int main() {
    ifstream input_file("C:/KLA_MOCK_HACKTHON/Student Handout/Input data/level0.json");
    if (!input_file.is_open()) {
        cerr << "Error opening input file!" << endl;
        return 1;
    }

    json input_data;
    input_file >> input_data;

    int nNeighbourhoods = input_data["n_neighbourhoods"];
    int startLocation = 0;  // Assuming the restaurant is at location 0

    unordered_map<string, vector<int>> distances;

    // Extract distances from JSON data
    for (const auto& entry : input_data["neighbourhoods"].items()) {
        const string& neighborhood = entry.key();
        const vector<int>& distance_array = entry.value()["distances"];
        distances[neighborhood] = distance_array;
    }

    vector<int> recommendedPath = recommendPath(nNeighbourhoods, startLocation, distances);

    cout << "Recommended Path:";
    for (int node : recommendedPath) {
        cout << " " << node;
    }
    cout << endl;

    return 0;
}
