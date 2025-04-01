#include "Puzzle/bfs.hpp"
#include "Puzzle/Heuristics.hpp"
#include <queue>
#include <unordered_set>
#include <iostream>

namespace Puzzle {
    SearchStats BFSSolver::solve(const State& initialState) {
        SearchStats stats;
        stats.startTimer();
        stats.setInitialHeuristic(Heuristics::manhattanDistance(initialState));

        if (initialState.isGoal()) {
            stats.stopTimer();
            return stats;
        }

        std::queue<State> open;
        std::unordered_set<State, StateHash> closed;

        initialState.printState();

        open.push(initialState);
        closed.insert(initialState);
        stats.updateMaxQueueSize(open.size());

        while (!open.empty()) {
            State current = open.front();
            open.pop();
            
            // Update statistics
            stats.nodeExpanded(Heuristics::manhattanDistance(current));
            
            for (const auto& neighbor : current.getNeighbors()) {
                if (neighbor.isGoal()) {
                    stats.stopTimer();
                    return stats;
                }
                
                if (closed.find(neighbor) == closed.end()) {
                    closed.insert(neighbor);
                    open.push(neighbor);
                    stats.updateMaxQueueSize(open.size());
                }
            }
        }
        
        stats.stopTimer();
        return stats;
    }
}