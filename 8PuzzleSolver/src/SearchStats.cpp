#include "Puzzle/SearchStats.hpp"
#include <iostream>
#include <iomanip>

namespace Puzzle {
    SearchStats::SearchStats() = default;

    void SearchStats::startTimer() {
        start_time = Clock::now();
    }

    void SearchStats::stopTimer() {
        search_time = Clock::now() - start_time;
    }

    void SearchStats::nodeExpanded(double heuristic_value) {
        ++expanded_nodes;
        total_heuristic += heuristic_value;
    }

    void SearchStats::updateMaxQueueSize(size_t current_size) {
        if(current_size > max_queue_size) {
            max_queue_size = current_size;
        }
    }

    void SearchStats::print() const {
        std::cout << std::fixed << std::setprecision(2)
                << "Search Statistics:\n"
                << "------------------\n"
                << "Expanded nodes:  " << expanded_nodes << "\n"
                << "Search time:     " << search_time.count() << "s\n"
                << "Initial heuristic: " << initial_h << "\n"
                << "Average heuristic: " << averageHeuristic() << "\n"
                << "Max queue size:  " << max_queue_size << "\n";
    }

    std::string SearchStats::csvHeader() const {
        return "expanded_nodes,search_time,initial_h,avg_h,max_queue_size";
    }

    std::string SearchStats::csvLine() const {
        return std::to_string(expanded_nodes) + "," 
            + std::to_string(search_time.count()) + ","
            + std::to_string(initial_h) + ","
            + std::to_string(averageHeuristic()) + ","
            + std::to_string(max_queue_size);
    };
}