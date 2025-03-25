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

/**
 * action := UP | LEFT | RIGHT | DOWN
 * Enumeration of possible actions in the 8Puzzle game.
 */
enum Action {UP, LEFT, RIGHT, DOWN};


std::vector<int> GOAL = {1, 2, 3, 4, 5, 6, 7, 8, 0};
// GOAL é o estado final do jogo.



/**
 * @brief Verifica se um estado é o estado final.
 *
 * @param state Vetor de 9 elementos inteiros representando o estado.
 * @return true se state for o estado final; false caso contrário.
 */
bool isGoal(std::vector<int> state) {
    for (int i = 0; i < 9; i++) {
        if (state[i] != GOAL[i]) {
            return false;
        };
    };
    return true;
};

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
 * @param state The current state of the puzzle board, represented as a vector of integers.
 * @param action The action that led to this node, represented as a string.
 * @param parent A pointer to the parent node.
 * @return A Node structure containing the state, action, and parent information.
 */
Node getNode(array::int state, Action action, Node* parent) {
    return {
        .state = state,
        .action = action,
        .parent = parent
    };
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
    Action action = UP;
    array::int state = {1, 2, 3, 4, 5, 6, 7, 0, 8};

    Node node = getNode(state, action, nullptr);

    printState(node);
};

