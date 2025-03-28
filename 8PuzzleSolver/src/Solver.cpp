/**
 *  @file       `Solver.cpp`
 *  @brief      Solver interface and implementations
 *  @details    Interface for solvers and implementations of local search solvers for the 8Puzzle game.
 *  @author     rdcn
 *  @date       2023-05-27
 *  @version    1.0
 */


#include "Solver.hpp"
#include "SearchNode.hpp"
#include "Heuristic.hpp"
#include <deque>
#include <unordered_set>
#include <chrono>
#include <algorithm>
#include <unordered_map>
#include <hash_set>
#include <functional>
#include <string>
#include <queue>
#include <thread>
#include <atomic>
#include <iostream>
using namespace std;

//  SearchResult

/**
 * @brief       Prints the solution metrics
 * 
 * Para cada estado inicial na entrada a sua implementa¸c˜ao devera apresentar em uma nova linha
separados por virgula: n´umero de nodos expandidos, comprimento da solu¸c˜ao ´otima, tempo
para solu¸c˜ao, valor m´edio da fun¸c˜ao heur´ıstica, valor da fun¸c˜ao heur´ıstica no estado inicial.
 * 
 * @param const SearchResult& result
 */
void SearchResult::print() const {
    cout << nodes_expanded << "," << solution_length << "," << time_seconds << "," << avg_heuristic << "," << initial_heuristic << endl;
}



/**
 * @brief Get the Neighbors object
 * 
 * @param s 
 * @return vector<pair<Action, PuzzleState>> 
 */
vector<pair<Action, PuzzleState>> getNeighbors(PuzzleState s) {
    vector<pair<Action, PuzzleState>> neighbors;
    int blank_pos = s.blank_pos;

    const int row = blank_pos / 3;
    const int col = blank_pos % 3;
    
    const int moves[4][2] = {{-1,0}, {0,-1}, {0,1}, {1,0}};
    const Action actions[4] = {Action::UP, Action::LEFT, Action::RIGHT, Action::DOWN};

    for (int i = 0; i < 4; ++i) {
        int new_row = row + moves[i][0];
        int new_col = col + moves[i][1];
        
        if (new_row >= 0 && new_row < 3 && new_col >= 0 && new_col < 3) {
            int new_pos = new_row * 3 + new_col;
            PuzzleState new_state = s;
            std::swap(new_state.tiles[blank_pos], new_state.tiles[new_pos]);
            new_state.blank_pos = new_pos;
            neighbors.emplace_back(actions[i], new_state);
        }
    }
    
    return neighbors;
}

SearchResult breadthFirstSearch(PuzzleState initial_state, Heuristic& heuristic) {
    SearchResult result;
    chrono::high_resolution_clock::time_point start_time = chrono::high_resolution_clock::now();
    result.initial_heuristic = heuristic.calculate(initial_state);

    // Check if initial state is the goal
    if (initial_state.isGoal()) {
        result.solution_length = 0;
        result.nodes_expanded = 0;
        result.total_heuristic = 0;
        result.avg_heuristic = 0.0;
        result.time_seconds = chrono::duration_cast<chrono::duration<double>>(chrono::high_resolution_clock::now() - start_time).count();
        return result;
    }

    deque<shared_ptr<Node>> open;
    unordered_set<PuzzleState, PuzzleState::Hash> closed;

    open.push_back(make_shared<Node>(initial_state, 0, heuristic.calculate(initial_state), Action::NONE, nullptr));
    closed.insert(initial_state);

    int niter = 0;
    result.total_heuristic = 0;

    while (!open.empty()) {
        ++niter;
        auto current = open.front();
        open.pop_front();

        result.total_heuristic += current->h;

        if (current->state.isGoal()) {
            result.solution_length = current->g;
            result.avg_heuristic = static_cast<double>(result.total_heuristic) / niter;
            result.time_seconds = chrono::duration_cast<chrono::duration<double>>(chrono::high_resolution_clock::now() - start_time).count();
            return result;
        }

        for (auto& neighbor : getNeighbors(current->state)) {
            if (!closed.count(neighbor.second)) {
                open.push_back(make_shared<Node>(neighbor.second, current->g + 1, heuristic.calculate(neighbor.second), neighbor.first, current));
                closed.insert(neighbor.second);
            }

            if (neighbor.second.isGoal()) {
                result.solution_length = current->g + 1;
                result.avg_heuristic = static_cast<double>(result.total_heuristic) / niter;
                result.time_seconds = chrono::duration_cast<chrono::duration<double>>(chrono::high_resolution_clock::now() - start_time).count();
                return result;
            }
        }
    }

    // If open is empty and no solution found
    result.solution_length = -1;
    result.nodes_expanded = niter;
    result.avg_heuristic = (niter == 0) ? 0.0 : static_cast<double>(result.total_heuristic) / niter;
    result.time_seconds = chrono::duration_cast<chrono::duration<double>>(chrono::high_resolution_clock::now() - start_time).count();
    return result;
}
