/**
 * @file    8Puzzle.c
 * @author  rdcn
 * @brief   Implementação do jogo 8Puzzle em C/C++
 * @version 1.0.0
 * @date    2025-03-25
 * @details O 8Puzzle é implementado como um vetor de 9 elementos inteiros, no qual
 *          o 0 representa o espaço vazio. Ao invés de movimentarmos as peças, movimentamos
 *          exclusivamente o espaço vazio (0).
 */

#include <iostream>
#include <vector>
#include <array>
#include <queue>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
#include <fstream>
#include <sstream>

/**
 * action := UP | LEFT | RIGHT | DOWN
 * Enumeration of possible actions in the 8Puzzle game.
 */
enum Action {UP, LEFT, RIGHT, DOWN};


std::vector<int> GOAL = {1, 2, 3, 4, 5, 6, 7, 8, 0};
// GOAL é o estado final do jogo.

//  Functions for analyzing the 8Puzzle game

/**
 * @brief   Given an `state`, returns the position of the empty space in the 8Puzzle game as a pair of integers.
 * 
 * @param state `const std::array<int, 9>&`
 *              The state of the 8Puzzle game.
 * 
 * @return `std::pair<int, int>`
 *         The position of the empty space in the 8Puzzle game as a pair of integers.
 */
std::pair<int, int> getEmptySpacePosition(const std::array<int, 9>& state) {
    int index = std::distance(state.cbegin(), std::find(state.cbegin(), state.cend(), 0));
    return std::make_pair(index / 3, index % 3);
}



/**
 * @brief   An 8Puzzle node consisting of a state (vector<int>), an action (string),
 *         and a parent (Node*).
 * 
 * @param state    The state of the node.
 * @param action   The action taken to get to this node.
 * @param parent   The parent of this node.
 */
struct Node {
    std::array<int, 9>  state;      //  Gamestate, the board
    Action              action;     //  Action to get to this node
    Node*               parent;     //  Parent node
};

/**
 * @brief Creates a new node for the 8Puzzle game.
 * 
 * @param state `std::array<int, 9>`
 *              A pointer to the state of the node.
 * @param action `Action`
 *              The action taken to get to this node.
 * @param parent `Node*`
 *              The parent of this node.
 * 
 * @return `Node`
 *         A new node for the 8Puzzle game.
 */
Node getNode(std::array<int, 9> state, Action action, Node* parent) {
    Node node;
    node.state = state;
    node.action = action;
    node.parent = parent;
    return node;
};

/**
 * @brief       Given a `Node` for the 8Puzzle game, returns a vector of neighboring nodes.
 * @details     The neighbors of a node are the nodes that can be reached by performing an action on the node.
 *              They are always generated in the order UP, LEFT, RIGHT, DOWN.
 * 
 * @param       `Node` node
 *              The `Node` for the 8Puzzle game.
 * 
 * @return      `std::vector<Node>`
 *              A vector of neighboring nodes.
 */
std::vector<Node> getNeighbors(const Node& node) {
    std::vector<Node> neighbors;
    const std::array<int, 4> dx = { -3, -1, 1, 3 };
    const std::array<Action, 4> actions = { Action::UP, Action::LEFT, Action::RIGHT, Action::DOWN };
    int emptySpaceIndex = std::distance(node.state.cbegin(), std::find(node.state.cbegin(), node.state.cend(), 0));
    for (int i = 0; i < 4; ++i) {
        int newIndex = emptySpaceIndex + dx[i];
        if (newIndex >= 0 && newIndex < 9 && (dx[i] % 3 == 0 || node.state[newIndex] != 0)) {
            std::array<int, 9> newState = node.state;
            std::swap(newState[emptySpaceIndex], newState[newIndex]);
            neighbors.emplace_back(getNode(newState, actions[i], const_cast<Node*>(&node)));
        }
    }
    return neighbors;
}

//  EVALUATION

/**
 * @brief   Misplaced tiles heuristic for the 8Puzzle game.
 *
 * @param   `std::array<int, 9>` state
 *          The state of the 8Puzzle game.
 * 
 * @return  `int`
 *          The number of misplaced tiles.
 */
int misplacedTiles(std::array<int, 9> state) {
    int score = 0;
    for (int i = 0; i < 9; i++) {
        if (state[i] != GOAL[i]) {
            score++;
        }
    }
    return score;
};

/**
 * @brief   Efficiently computes aprox. the Manhattan distance for two positions in a 3x3 grid.
 * 
 * @param   v `std::pair<int, int>`
 *          The first position.
 * @param   w `std::pair<int, int>`
 *          The second position.
 *
 * @return  `int`
 *          The Manhattan distance.
 */
int manhattan(std::pair<int, int> v, std::pair<int, int> w) { return std::abs(v.first - w.first) + std::abs(v.second - w.second); }

/**
 * @brief       Wrapper around the `manhattan` function for the 8Puzzle game.
 * @details     Takes the goal to be the first position of the 8Puzzle game.
 * 
 * @param       pos `std::pair<int, int>`
 *              The position of the tile.
 * 
 * @return      `int`
 *              The Manhattan distance to the goal.
 */
int manhattan(std::pair<int, int> pos) { return manhattan(pos, {0, 0}); }

/**
 * @brief   Manhattan distance heuristic for the 8Puzzle game.
 *
 * @param   state The state of the 8Puzzle game.
 *
 * @return  The Manhattan distance.
 */
int manhattanDistance(const std::array<int, 9>& state) {
    static const std::array<std::pair<int, int>, 9> goalPositions = {
        {{0, 0}, {1, 0}, {2, 0}, {0, 1}, {1, 1}, {2, 1}, {0, 2}, {1, 2}, {2, 2}}
    };
    int distance = 0;
    for (int i = 0; i < 9; ++i) {
        if (state[i] != 0) {
            int x1 = i % 3;
            int y1 = i / 3;
            int x2 = goalPositions[state[i]].first;
            int y2 = goalPositions[state[i]].second;
            distance += std::abs(x1 - x2) + std::abs(y1 - y2);
        }
    }
    return distance;
}

/**
 * @brief   Given an `Node` node, evaluates its `state` and returns a score.
 * 
 * @param   `Node` node
 *          The `Node` for the 8Puzzle game.
 * 
 * @return  `int`
 *          The score of the node.
 */
int evaluate(Node node) {
    return misplacedTiles(node.state);
};


/**
 * @brief Prints the state (gamestate, 8Puzzle board) of a `Node` object.
 * 
 * @param node The `Node` object whose state is to be printed.
 */
void printState(Node node) {
    for (int i = 0; i < 9; i++) {
        std::cout << node.state[i] << " ";
        if ((i + 1) % 3 == 0) {
            std::cout << std::endl;
        };
    };
    std::cout << std::endl;
};


int main() {
    const Action action = Action::UP;
    std::array<int, 9> initialState = {1, 2, 3, 4, 5, 6, 7, 0, 8};
    Node node = getNode(initialState, action, nullptr);

    const auto emptySpacePosition = getEmptySpacePosition(node.state);
    std::cout << "(" << emptySpacePosition.first << ", " << emptySpacePosition.second << ")" << std::endl;
    
    std::vector<Node> neighbors = getNeighbors(node);
    for (Node neighbor : neighbors) {
        //  Evaluation
        int score = evaluate(neighbor);
        std::cout << "Misplaced Tiles: " << score <<  "Manhattan Distance: " << manhattanDistance(neighbor.state) << std::endl;
        std::vector<Node> neighbors2 = getNeighbors(neighbor);

        for (Node neighbor2 : neighbors2) {
            int score2 = evaluate(neighbor2);
            std::cout << "Misplaced Tiles: " << score2 <<  "Manhattan Distance: " << manhattanDistance(neighbor2.state) << std::endl;
        };
    };

    return 0;
};

