#pragma once
#include "PuzzleState.hpp"

namespace Puzzle {
    /**
     * @brief       The `Heuristics` namespace contains functions for heuristic evaluation of the 8Puzzle game.
     */
    namespace Heuristics {
        int manhattanDistance(const State& state);
        int misplacedTiles(const State& state);
        int linearConflict(const State& state);
    };
}