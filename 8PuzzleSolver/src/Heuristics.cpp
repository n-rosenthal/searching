#include "Puzzle/Heuristics.hpp"
#include "Puzzle/PuzzleState.hpp"
#include <cmath>

namespace Puzzle::Heuristics {
    int manhattanDistance(const State& state) {
        const auto& tiles = state.getTiles();
        int distance = 0;
        
        for (size_t i = 0; i < State::SIZE; ++i) {
            const int value = tiles[i];
            if (value == 0) continue;
            
            const int targetRow = (value - 1) / 3;
            const int targetCol = (value - 1) % 3;
            const int currentRow = i / 3;
            const int currentCol = i % 3;
            
            distance += abs(targetRow - currentRow) + 
                       abs(targetCol - currentCol);
        }
        return distance;
    }

    int misplacedTiles(const State& state) {
        const auto& tiles = state.getTiles();
        int count = 0;
        for (size_t i = 0; i < State::SIZE - 1; ++i) {
            if (tiles[i] != static_cast<int>(i + 1)) count++;
        }
        if (tiles.back() != 0) count++;
        return count;
    }
}