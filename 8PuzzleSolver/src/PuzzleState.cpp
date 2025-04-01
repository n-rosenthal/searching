#include "Puzzle/PuzzleState.hpp"
#include <stdexcept>
#include <string>
#include <vector>
#include <algorithm>
#include <iostream>

namespace Puzzle {
    bool State::isValidState(const Grid& tiles) {
        if (tiles.size() != SIZE) {
            return false;
        }
        return true;
    };
    
    State::State(const Grid& tiles, State* parent) : tiles_(tiles), parent_(parent) {
        if (!isValidState(tiles)) {
            throw std::invalid_argument("Invalid state");
        };

    }

    bool State::isGoal() const {
        const Grid GOAL = {0,1,2,3,4,5,6,7,8};
        return tiles_ == GOAL;
    }

    /**
     * @brief       Prints the state of the 8Puzzle game in a linear format.
     */
    void State::printState() const {
        for (int i = 0; i < SIZE; i++) {
            std::cout << tiles_[i] << " ";
        }
        std::cout << std::endl;
    };


    std::vector<State> State::getNeighbors() const {
        std::vector<State> neighbors;
        int blankPos = blankPosition();
        //  up
        if (blankPos >= 3) {
            State neighbor = *this;
            neighbor.swapTiles(blankPos, blankPos - 3);
            neighbor.setParent(const_cast<State*>(this));
            neighbors.push_back(neighbor);
        };

        //  left
        if (blankPos % 3 != 0) {
            State neighbor = *this;
            neighbor.swapTiles(blankPos, blankPos - 1);
            neighbor.setParent(const_cast<State*>(this));
            neighbors.push_back(neighbor);
        };

        //  right
        if (blankPos % 3 != 2) {
            State neighbor = *this;
            neighbor.swapTiles(blankPos, blankPos + 1);
            neighbor.setParent(const_cast<State*>(this));
            neighbors.push_back(neighbor);
        };

        //  down
        if (blankPos < 6) {
            State neighbor = *this;
            neighbor.swapTiles(blankPos, blankPos + 3);
            neighbor.setParent(const_cast<State*>(this));
            neighbors.push_back(neighbor);
        };

        return neighbors;
    };
    

    size_t State::blankPosition() const {
        auto it = std::find(tiles_.begin(), tiles_.end(), 0);
        return std::distance(tiles_.begin(), it);
    }

    bool State::operator==(const State& other) const {
        return tiles_ == other.tiles_;
    }

    bool State::operator<(const State& other) const {
        return tiles_ < other.tiles_;
    }

    void State::swapTiles(size_t i, size_t j) {
        std::swap(tiles_[i], tiles_[j]);
    }


    /**
     * @brief       Gets the path from the start state to the goal state.
     * 
     * @return      std::vector<State>
     */
    std::vector<State> State::getPath() const {
        std::vector<State> path;
        const State* current = this;
        while (current != nullptr) {
            path.push_back(*current);
            current = current->parent_;
        }
        std::reverse(path.begin(), path.end());
        return path;
    }

    size_t StateHash::operator()(const State& state) const {
        const auto& tiles = state.getTiles();
        size_t hash = 0;
        for (int tile : tiles) {
            hash = (hash << 4) | (hash >> (sizeof(size_t)*8 - 4));
            hash ^= tile + 0x9e3779b9 + (hash << 6) + (hash >> 2);
        }
        return hash;
    }
}