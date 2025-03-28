/**
 * @file        `SearchNode.cpp`
 * @author      rdcn
 * @brief       Search node implementation
 * @version     1.0
 * @date        2025-03-27
 */

#include "SearchNode.hpp"
#include <vector>

/**
 * @brief       Constructs a `SearchNode` with the given game state, path cost, heuristic estimate, action, and parent node.
 * 
 * @param       `PuzzleState` s
 *              The game state of the node.
 * @param       `int` g_val
 *              The path cost from the start state to the current state.
 * @param       `int` h_val
 *              The heuristic estimate for the current state.
 * @param       `Action` act
 *              The action that led to the current state.
 * @param       `std::shared_ptr<Node>` p
 *              The parent node of the current node.
 * 
 * @return      A `SearchNode` object.
 */
Node::Node(PuzzleState s, int g_val, int h_val, Action act, std::shared_ptr<Node> p) : state(s), g(g_val), h(h_val), action(act), parent(p) {};

