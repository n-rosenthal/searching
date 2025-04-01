#pragma once
#include "PuzzleState.hpp"
#include "SearchStats.hpp"

namespace Puzzle {
    class BFSSolver {
    public:
        SearchStats solve(const State& initialState);
    };
} // namespace Puzzle