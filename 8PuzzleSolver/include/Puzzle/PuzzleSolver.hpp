#pragma once
#include "PuzzleState.hpp"
#include "Heuristics.hpp"
#include "SearchStats.hpp"
#include <queue>
#include <unordered_set>

namespace Puzzle {
    class Solver {
    public:
        const SearchStats& getStats() const { return stats; }

        struct Node {
            State state;
            int cost;
            int heuristic;
            
            bool operator>(const Node& other) const {
                return (cost + heuristic) > (other.cost + other.heuristic);
            }
        };

        std::vector<State> solve(const State& initial);
        
    private:
        SearchStats stats;
        
        using PriorityQueue = std::priority_queue<
            Node, 
            std::vector<Node>,
            std::greater<>
        >;
        
        std::unordered_set<State, StateHash> closedSet;
    };
}