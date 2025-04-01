#include "Puzzle/PuzzleSolver.hpp"
#include <unordered_map>
#include <vector>
#include <algorithm>

namespace Puzzle {
    std::vector<State> Solver::solve(const State& initial) {
        PriorityQueue open;
        std::unordered_map<State, int, StateHash> costSoFar;
        std::unordered_map<State, State, StateHash> cameFrom;

        open.push({initial, 0, Heuristics::manhattanDistance(initial)});
        costSoFar[initial] = 0;

        while (!open.empty()) {
            const Node current = open.top();
            open.pop();

            if (current.state.isGoal()) {
                // Reconstruct path
                std::vector<State> path;
                State currentState = current.state;
                while (cameFrom.find(currentState) != cameFrom.end()) {
                    path.push_back(currentState);
                    currentState = cameFrom[currentState];
                }
                path.push_back(initial);
                std::reverse(path.begin(), path.end());
                return path;
            }

            for (const auto& neighbor : current.state.getNeighbors()) {
                const int newCost = current.cost + 1;
                if (!costSoFar.count(neighbor) || newCost < costSoFar[neighbor]) {
                    costSoFar[neighbor] = newCost;
                    cameFrom.emplace(neighbor, current.state);
                    const int priority = newCost + Heuristics::manhattanDistance(neighbor);
                    open.push({neighbor, newCost, priority - newCost});
                }
            }
        }
        
        return {}; // No solution
    }
}