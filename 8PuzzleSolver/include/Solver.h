/**
 *  @file       `Solver.h`
 *  @brief      Solver interface and implementations
 *  @details    Interface for solvers and implementations of local search solvers for the 8Puzzle game.
 *  @author     rdcn
 *  @date       2023-05-27
 *  @version    1.0
 */

#pragma once
#include "PuzzleState.h"
#include "SearchNode.h"
#include "Heuristic.h"
#include <chrono>
#include <memory>
#include <unordered_set>
#include <functional>

using namespace std;

/**
 * @struct SearchResult
 * @brief Contains solution metrics
 */
struct SearchResult {
    int nodes_expanded;      ///< Total nodes expanded
    int solution_length;     ///< Number of moves in solution
    double time_seconds;     ///< Execution time in seconds
    double avg_heuristic;    ///< Average heuristic value
    int initial_heuristic;   ///< Heuristic value of initial state
};

/**
 * @brief       Implements the `PuzzleSolver` interface.
 * @details     Each solver will use the interface, but
 *              1.  'bfs' uses 
 *                  a.  `BreadthFirstSearch` as the search algorithm
 *                  b.  queue as the open list
 *                  c.  unordered_set as the closed set
 *              2.  'astar' uses 
 *                  a.  `AStarSearch` as the search algorithm
 *                  b.  priority_queue as the open list
 *                  c.  unordered_set as the closed set
 */
class PuzzleSolver {
public:
    virtual SearchResult solve(const PuzzleState& initial, Heuristic& heuristic, bool use_heuristic) = 0;
};
