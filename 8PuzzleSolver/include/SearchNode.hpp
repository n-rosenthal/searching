/**
 * @file        `SearchNode.hpp`
 * @brief       Search node structure for graph search
 * @details     The `Node` struct represents a node in a search tree/graph. It contains the game state, path cost, heuristic estimate, action that led to the state, and a pointer to the parent node.
 * 
 * @author      rdcn
 * @date        2023-05-27
 * @version     1.0
 */

 #pragma once
 #include "PuzzleState.hpp"
 #include <memory>
 
 /**
  * @struct Node
  * @brief Node in the search tree/graph
  */
 struct Node {
     PuzzleState state;              ///< Game state
     int g;                          ///< Path cost from start
     int h;                          ///< Heuristic estimate
     Action action;                  ///< Action that led to this state
     std::shared_ptr<Node> parent;   ///< Parent node pointer
 
     Node(PuzzleState s, int g_val, int h_val, Action act, std::shared_ptr<Node> p);
 };