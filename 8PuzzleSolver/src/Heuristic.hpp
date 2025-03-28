/**
 * @file        `Heuristic.hpp`
 * @brief       Heuristic function interface and implementations
 * @details     Heuristic functions estimate the cost to reach the goal state from a given state. The current implementation includes the Manhattan distance heuristic only.
 * 
 * @author      rdcn
 * @date        2023-05-27
 * @version     1.0
 */

 #pragma once
 #include "PuzzleState.hpp"
 #include <array>

using namespace std;


/**
 * @class       Heuristic
 * @brief       Interface for a heuristic function.
 * 
 * @details     A heuristic function estimates the cost to reach the goal state from a given state.
 *              The `calculate` method must be implemented by derived classes.
 *              The `average` method returns the average value of the heuristic over all states that have been evaluated so far.
 */
class Heuristic {
    public:
        virtual int calculate(const PuzzleState&) const = 0;
        virtual int average() const { return total / count; }
        virtual ~Heuristic() = default;
        mutable int total = 0;
        mutable int count = 0;
};

class ManhattanHeuristic : public Heuristic {
    public:
        static const array<int, 9> GOAL_POS;
        int calculate(const PuzzleState& s) const override;
        ~ManhattanHeuristic() override = default;
        int manhattan(int x1, int y1, int x2, int y2) const;
};
