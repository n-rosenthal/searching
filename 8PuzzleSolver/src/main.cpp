#include "Puzzle/PuzzleSolver.hpp"
#include "Puzzle/Heuristics.hpp"
#include "Puzzle/PuzzleState.hpp"
#include "Puzzle/SearchStats.hpp"

//  Search Algorithm Solvers
#include "Puzzle/bfs.hpp"
#include "Puzzle/dfs.hpp"
#include "Puzzle/iterative_deepening.hpp"

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <chrono>
#include <sstream>


int main(int argc, char* argv[]) {
    //  State initialization
    Puzzle::State s = Puzzle::State({5, 0, 2, 6, 4, 8, 1, 7, 3});
    s.printState();

    //  Neighbors
    std::vector<Puzzle::State> neighbors = s.getNeighbors();
    for (auto neighbor : neighbors) {
        neighbor.printState();
    };

    //  Solve it using bfs
    Puzzle::BFSSolver bfsSolver = Puzzle::BFSSolver();
    try {
        Puzzle::BFSSolver bfsSolver;
        Puzzle::SearchStats bfsStats = bfsSolver.solve(s);
        bfsStats.print();
        
        // Existing solution printing code...
    } catch (const std::exception& e) {
        // ... error handling ...
    };

    //  Solve it using dfs
    Puzzle::DFSSolver dfsSolver = Puzzle::DFSSolver();
    try {
        Puzzle::DFSSolver dfsSolver;
        Puzzle::SearchStats dfsStats = dfsSolver.solve(s);
        dfsStats.print();
        
        // Existing solution printing code...
    } catch (const std::exception& e) {
        // ... error handling ...
    };

    //  Solve it using iterative deepening
    Puzzle::IDSolver idsSolver = Puzzle::IDSolver();
    try {
        Puzzle::IDSolver idsSolver;
        Puzzle::SearchStats idsStats = idsSolver.solve(s);
        idsStats.print();
        
        // Existing solution printing code...
    } catch (const std::exception& e) {
        // ... error handling ...
    };
}
