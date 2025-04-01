#include "Puzzle/iterative_deepening.hpp"
#include "Puzzle/Heuristics.hpp"
#include "Puzzle/PuzzleState.hpp"
#include <queue>
#include <unordered_set>
#include <iostream>

namespace Puzzle {

SearchStats IDSolver::solve(const State& initialState) {
    SearchStats stats;
    stats.startTimer();
    stats.setInitialHeuristic(Heuristics::manhattanDistance(initialState));

    if (initialState.isGoal()) {
        stats.stopTimer();
        return stats;
    };

    std::queue<State> open;
    std::unordered_set<State, StateHash> closed;
    int depth = 0;

    open.push(initialState);
    closed.insert(initialState);

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

            if (!closed.count(neighbor)) {
                open.push(neighbor);
                closed.insert(neighbor);
            }
        }

        if (open.size() > depth) {
            depth = open.size();
            stats.updateMaxQueueSize(depth);
        }
    }

    stats.stopTimer();
    return stats;
};

};