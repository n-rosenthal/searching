/**
 * @file main.cpp
 * @brief Main program entry point
 */

 #include "Heuristic.hpp"
 #include "PuzzleState.hpp"
 #include "SearchNode.hpp"
 #include <memory>
 #include "Solver.hpp"
 #include <array>
 #include <iostream>

using namespace std;

 int main(int argc, char* argv[]) {
   // test if solution is goal
   PuzzleState goal_state({1,2,3,4,5,6,7,8,0});

   if (goal_state.isGoal()) {
       cout << "Goal state is goal" << endl;
   }


    // 0 6 1 7 4 2 3 8 5, 5 0 2 6 4 8 1 7 3, 2 4 7 0 3 6 8 1 5
    vector<PuzzleState> puzzles = {
        PuzzleState({0,6,1,7,4,2,3,8,5}), PuzzleState({5,0,2,6,4,8,1,7,3}), PuzzleState({2,4,7,0,3,6,8,1,5})
    };

    ManhattanHeuristic heuristic = ManhattanHeuristic();

    for (const auto& puzzle : puzzles) {
        SearchResult result = breadthFirstSearch(puzzle, heuristic);
        result.print();
    }
};