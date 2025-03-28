/**
 * @file        `Heuristic.h`
 * @brief       Heuristic function interface and implementations
 * @details     Heuristic functions estimate the cost to reach the goal state from a given state. The current implementation includes the Manhattan distance heuristic only.
 * 
 * @author      rdcn
 * @date        2023-05-27
 * @version     1.0
 */

 #pragma once
 #include "PuzzleState.h"
 
 /**
  * @class      Heuristic
  * @brief      Interface for heuristic functions
  */
 class Heuristic {
 public:
     mutable int total = 0;  ///< Sum of all heuristic values
     mutable int count = 0;  ///< Number of evaluations
     
     virtual int calculate(const PuzzleState&) const = 0;
     virtual ~Heuristic() = default;
     double average() const;
 };
 
 /**
  * @class ManhattanHeuristic
  * @brief Manhattan distance heuristic implementation
  */
 class ManhattanHeuristic : public Heuristic {
 public:
     static const std::array<int, 9> GOAL_POS;
     int calculate(const PuzzleState& s) const override;
 };