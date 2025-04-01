#pragma once
#include "PuzzleState.hpp"
#include "SearchStats.hpp"

namespace Puzzle {
    class DFSSolver {
    public:
        SearchStats solve(const State& initialState);
    };
};