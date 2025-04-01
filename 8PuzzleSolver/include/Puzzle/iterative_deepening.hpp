#pragma once
#include "PuzzleState.hpp"
#include "SearchStats.hpp"

namespace Puzzle {
    class IDSolver {
    public:
        SearchStats solve(const State& initialState);
    

    private:
        SearchStats stats;
        int max_depth;
        int current_depth;

    };
};