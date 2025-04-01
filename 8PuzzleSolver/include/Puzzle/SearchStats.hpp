#pragma once
#include <chrono>
#include <string>
#include <iostream>
#include <vector>

#include "PuzzleState.hpp"


namespace Puzzle {
    class SearchStats {
    public:
        SearchStats();
        
        // Timing control
        void startTimer();
        void stopTimer();
        
        // Metrics updates
        void nodeExpanded(double heuristic_value);
        void updateMaxQueueSize(size_t current_size);
        
        // Reporting
        void print() const;
        std::string csvHeader() const;
        std::string csvLine() const;

        // Accessors
        size_t expandedNodes() const { return expanded_nodes; }
        double searchTime() const { return search_time.count(); }
        double initialHeuristic() const { return initial_h; }
        double averageHeuristic() const { return total_heuristic / expanded_nodes; }
        size_t maxQueueSize() const { return max_queue_size; }

        void setInitialHeuristic(double h) { initial_h = h; }

        //  Copy semantics
        SearchStats(const SearchStats&) = default;
        SearchStats& operator=(const SearchStats&) = default;

        //  Move semantics
        SearchStats(SearchStats&&) = default;
        SearchStats& operator=(SearchStats&&) = default;

        ~SearchStats() = default;


    private:
        using Clock = std::chrono::high_resolution_clock;
        using TimePoint = std::chrono::time_point<Clock>;
        using Duration = std::chrono::duration<double>;

        // Core metrics
        size_t expanded_nodes = 0;
        double total_heuristic = 0.0;
        double initial_h = 0.0;
        size_t max_queue_size = 0;
        
        // Timing
        TimePoint start_time;
        Duration search_time;
        //  Retains the path from the goal to the initial state for reconstruction
        std::vector<Puzzle::State> path;
    };
} // namespace Puzzle