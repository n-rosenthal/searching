#include "Puzzle/dfs.hpp"
#include "Puzzle/Heuristics.hpp"
#include <stack>
#include <unordered_set>
#include <iostream>

namespace Puzzle {
    SearchStats DFSSolver::solve(const State& initialState) {
        SearchStats stats;
        stats.startTimer();
        stats.setInitialHeuristic(Heuristics::manhattanDistance(initialState));

        if (initialState.isGoal()) {
            stats.stopTimer();
            return stats;
        };

        std::stack<State> open;
        std::unordered_set<State, StateHash> closed;

        initialState.printState();

        open.push(initialState);
        closed.insert(initialState);
        stats.updateMaxQueueSize(open.size());

        while (!open.empty()) {
            State current = open.top();
            open.pop();

            // Update statistics
            stats.nodeExpanded(Heuristics::manhattanDistance(current));

            for (const auto& neighbor : current.getNeighbors()) {
                if (neighbor.isGoal()) {
                    stats.stopTimer();
                    return stats;
                };

                if (closed.find(neighbor) == closed.end()) {
                    open.push(neighbor);
                    closed.insert(neighbor);
                };
            };
        };

        return stats;
    };
};