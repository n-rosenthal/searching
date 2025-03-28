/**
 * @file        `Heuristic.cpp`
 * @author      rdcn
 * @brief       Heuristic function interface and concrete implementations
 * @details     This file implements the interface for heuristic functions and provides implementations of the Manhattan distance heuristic.
 * @version     1.0
 * @date        2025-03-27
 */

#include "Heuristic.hpp"
#include <array>
#include <algorithm>

using namespace std;

const array<int, 9> ManhattanHeuristic::GOAL_POS = {0, 1, 2, 3, 4, 5, 6, 7, 8};


/**
 * @brief   Manhattan distance heuristic for the 8Puzzle game.
 *
 * @param   state The state of the 8Puzzle game.
 *
 * @return  The Manhattan distance.
 */
int ManhattanHeuristic::calculate(const PuzzleState& s) const {
    int value = 0;
    for (int i = 0; i < 9; ++i) {
        //  indices of the goal state
        int goal_x = GOAL_POS[i] % 3;
        int goal_y = GOAL_POS[i] / 3;
        int x = s.tiles[i] % 3;
        int y = s.tiles[i] / 3;
        value += manhattan(x, y, goal_x, goal_y);
    }
    return value;
};

int ManhattanHeuristic::manhattan(int x1, int y1, int x2, int y2) const {
    return abs(x1 - x2) + abs(y1 - y2);
}