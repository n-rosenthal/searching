#pragma once
#include <array>
#include <vector>
#include <cstddef>

/**
 * @brief       The `Puzzle` namespace contains classes and functions related to the 8Puzzle game.
 * 
 */
namespace Puzzle {
    /**
     * @brief       Represents a state in the 8Puzzle game.
     * @details     The `State` class encapsulates the layout of tiles in the puzzle
     *              and provides functionality to manipulate and evaluate the state.
     */
    class State {
    public:
        /**
         * @brief       Default constructor for the `State` class.
         * @details     Initializes an empty state with no parent.
         */
        State() = default;

        static constexpr size_t SIZE = 9;       ///< Size of the 8Puzzle game
        using Grid = std::array<int, SIZE>;     ///< Type alias for the grid

        /**
         * @brief       Constructor for the `State` class.
         * @details     Constructs a state with a specified grid of tiles and an optional parent state.
         * 
         * @param       tiles
         *              `Grid` object representing the current state of the 8Puzzle game. 
         * @param       parent
         *              Pointer to the parent state, if any (default is nullptr).
         */
        explicit State(const Grid& tiles, State* parent = nullptr);

        /**
         * @brief       Checks if the current state is the goal state.
         * 
         * @return      `true` if the state is goal, `false` otherwise.
         */
        bool isGoal() const;

        /**
         * @brief       Generates neighboring states by moving the blank tile.
         * 
         * @return      A vector of neighboring `State` objects.
         */
        std::vector<State> getNeighbors() const;

        /**
         * @brief       Gets the position of the blank tile in the grid.
         * 
         * @return      The index of the blank tile.
         */
        size_t blankPosition() const;

        /**
         * @brief       Equality operator for `State` objects.
         * 
         * @param       other
         *              The `State` object to compare with.
         * 
         * @return      `true` if the states are equal, `false` otherwise.
         */
        bool operator==(const State& other) const;

        /**
         * @brief       Less-than operator for `State` objects.
         * 
         * @param       other
         *              The `State` object to compare with.
         * 
         * @return      `true` if the state is less than the other, `false` otherwise.
         */
        bool operator<(const State& other) const;

        /**
         * @brief       Retrieves the grid of tiles.
         * 
         * @return      A constant reference to the grid of tiles.
         */
        const Grid& getTiles() const { return tiles_; }

        /**
         * @brief       Prints the current state of the puzzle.
         */
        void printState() const;

        /**
         * @brief       Validates the provided grid of tiles.
         * 
         * @param       tiles
         *              The grid to validate.
         * 
         * @return      `true` if the grid is valid, `false` otherwise.
         */
        bool isValidState(const Grid& tiles);

        /**
         * @brief       Gets the parent of the current state.
         * 
         * @return      Pointer to the parent state.
         */
        State* getParent() const { return parent_; }

        /**
         * @brief       Sets the parent of the current state.
         * 
         * @param       parent
         *              Pointer to the parent state.
         */
        void setParent(State* parent) { parent_ = parent; }

        /**
         * @brief       Retrieves the path from the initial state to the current state.
         * 
         * @return      A vector of `State` objects representing the path.
         */
        std::vector<State> getPath() const;

    private:
        Grid tiles_;               ///< Grid representing the current state
        mutable State* parent_;    ///< Pointer to the parent state, mutable to allow changes in const methods

        /**
         * @brief       Swaps two tiles in the grid.
         * 
         * @param       i
         *              Index of the first tile.
         * @param       j
         *              Index of the second tile.
         */
        void swapTiles(size_t i, size_t j);

        /**
         * @brief       Checks if a move is valid.
         * 
         * @param       dx
         *              Change in x direction.
         * @param       dy
         *              Change in y direction.
         * 
         * @return      `true` if the move is valid, `false` otherwise.
         */
        bool isValidMove(int dx, int dy) const;
    };
    

    /**
     * @brief       Hash function for the `State` class.
     * 
     * @param       state
     *              The `State` object to hash.
     * 
     * @return      The hash value of the `State` object.
     * 
     */
    struct StateHash {
        size_t operator()(const State& state) const;
    };
}