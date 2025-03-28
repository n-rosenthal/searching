/**
 * @file        PuzzleState.hpp
 * @brief       Defines the `PuzzleState` class representing game states.
 * @details     The `PuzzleState` class represents a game state in the 8-Puzzle. It contains a board configuration (0=blank) and the position of the blank tile (0-8). The `PuzzleState` class also provides a hash value for the state and an equality operator to compare two states. This hash is computed by multiplying the hash value of each tile by 31 and adding the hash value of the blank tile.
 * 
 * @author      rdcn
 * @date        2023-05-27
 * @version     1.0
 */

 #pragma once
 #include <array>
 #include <unordered_set>
 #include <utility>

 
 enum class Action { UP, LEFT, RIGHT, DOWN, NONE };
 
 /**
  * @class      `PuzzleState`
  * @brief      Represents a game state in the 8-Puzzle
  */
 struct PuzzleState {
     std::array<int, 9> tiles;  ///< Board configuration (0=blank)
     int blank_pos;             ///< Position of blank tile (0-8)
     int hash_value;            ///< Precomputed hash value
 
     PuzzleState(const std::array<int, 9>& t);
     bool operator==(const PuzzleState& other) const;
     int computeHash() const;
     bool isGoal() const { return tiles == std::array<int, 9>{0, 1, 2, 3, 4, 5, 6, 7, 8}; };
     std::pair<int, int> getEmptySpace() const { return std::make_pair(blank_pos / 3, blank_pos % 3); };
     void print() const;

     struct Hash {
         size_t operator()(const PuzzleState& s) const;
     };
 };