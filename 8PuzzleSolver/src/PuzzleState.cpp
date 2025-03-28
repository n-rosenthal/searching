/**
 * @file        `PuzzleState.cpp`
 * @author      rdcn
 * @brief       PuzzleState class implementation
 * @version     1.0
 * @date        2025-03-27
 */

#include "PuzzleState.hpp"
#include <algorithm>
#include <unordered_set>
#include <numeric>

using namespace std;

/**
 * @brief       Constructs a `PuzzleState` from a given array of 9 tiles.
 * @details     The constructed `PuzzleState` has a precomputed `hash_value` and a `blank_pos` set to the position of the blank tile (0).
 * @param       `const std::array<int, 9>&` t
 *              The array of 9 tiles to construct the `PuzzleState` from.
 */
PuzzleState::PuzzleState(const std::array<int, 9>& t) : tiles(t) {
    hash_value = computeHash();
    blank_pos = static_cast<int>(distance(tiles.begin(), find(tiles.begin(), tiles.end(), 0)));
};

/**
 * @brief       Compares two `PuzzleState` objects for equality.
 *              The objects are compared by comparing their `tiles` arrays.
 * 
 * @param       `const PuzzleState&` other
 *              The other `PuzzleState` to compare with. 
 * 
 * @return      `bool`
 *              `true` if the two `PuzzleState` objects are equal, `false` otherwise.
 */
bool PuzzleState::operator==(const PuzzleState& other) const { return tiles == other.tiles; };


/**
 * @brief       Computes the hash value of the `PuzzleState` object.
 *              The hash value is computed by multiplying the hash value of each tile by 31 and adding the hash value of the empty tile.
 * 
 * @return      `int`
 *              The computed hash value.
 */
int PuzzleState::computeHash() const {
    int hash = 0;
    for (int tile : tiles) hash = hash * 31 + tile;
    return hash;
};


/**
 * @brief       Computes the hash value of the `PuzzleState` object.
 *              The hash value is computed by multiplying the hash value of each tile by 31 and adding the hash value of the empty tile.
 * 
 * @param       `const PuzzleState&` s
 *              The `PuzzleState` object to compute the hash value for.
 * 
 * @return      `size_t`
 *              The computed hash value.
 */
size_t PuzzleState::Hash::operator()(const PuzzleState& s) const { return s.hash_value; };


#include <iostream>

/**
 * @brief       Prints a `PuzzleState` object to the console.
 *              The `PuzzleState` object is printed as a 3x3 grid of tiles.
 * 
 * @param       `const PuzzleState&` s
 *              The `PuzzleState` object to print.
 * 
 * @return      `void`
 */
void PuzzleState::print() const {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            std::cout << tiles[i * 3 + j] << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
};
