#include <iostream>
#include <vector>
#include <array>
#include <queue>
#include <unordered_set>
#include <memory>
#include <chrono>
#include <sstream>
#include <algorithm>
#include <stdexcept>
#include <functional>
#include <unordered_map>
#include <string>

using namespace std;
using Clock = chrono::high_resolution_clock;

// ====================== Core Data Structures ======================
enum class Action { UP, LEFT, RIGHT, DOWN, NONE };

struct PuzzleState {
    array<int, 9> tiles;
    int blank_pos;
    int hash_value;

    PuzzleState(const array<int, 9>& t) : tiles(t) {
        blank_pos = static_cast<int>(distance(tiles.begin(), find(tiles.begin(), tiles.end(), 0)));
        hash_value = computeHash();
    }

    bool operator==(const PuzzleState& other) const { return tiles == other.tiles; }

    int computeHash() const {
        int hash = 0;
        for (int tile : tiles) hash = hash * 31 + tile;
        return hash;
    }

    struct Hash {
        size_t operator()(const PuzzleState& s) const { return s.hash_value; }
    };
};

// ====================== Heuristic ======================
class Heuristic {
public:
    mutable int total = 0;
    mutable int count = 0;
    
    virtual int calculate(const PuzzleState&) const = 0;
    virtual ~Heuristic() = default;
    
    double average() const { 
        return count > 0 ? static_cast<double>(total)/count : 0.0;
    }
};

class ManhattanHeuristic : public Heuristic {
public:
    static const array<int, 9> GOAL_POS;
    
    int calculate(const PuzzleState& s) const override {
        int distance = 0;
        for (int i = 0; i < 9; ++i) {
            if (s.tiles[i] == 0) continue;
            int goal_pos = GOAL_POS[s.tiles[i]-1];
            distance += abs(i/3 - goal_pos/3) + abs(i%3 - goal_pos%3);
        }
        total += distance;
        count++;
        return distance;
    }
};
const array<int, 9> ManhattanHeuristic::GOAL_POS = {0,1,2,3,4,5,6,7,8};

// ====================== Search Nodes ======================
struct Node {
    PuzzleState state;
    int g;
    int h;
    Action action;
    shared_ptr<Node> parent;

    Node(PuzzleState s, int g_val, int h_val, Action act, shared_ptr<Node> p)
        : state(s), g(g_val), h(h_val), action(act), parent(p) {}
};

// ====================== Open List Interface ======================
class OpenList {
public:
    virtual ~OpenList() = default;
    virtual void push(shared_ptr<Node> node) = 0;
    virtual shared_ptr<Node> pop() = 0;
    virtual bool empty() const = 0;
};

// ====================== Algorithm-Specific Open Lists ======================
class BFSOpenList : public OpenList {
    queue<shared_ptr<Node>> q;
public:
    void push(shared_ptr<Node> node) override { q.push(node); }
    shared_ptr<Node> pop() override { auto n = q.front(); q.pop(); return n; }
    bool empty() const override { return q.empty(); }
};

class AStarOpenList : public OpenList {
    struct Compare { bool operator()(const shared_ptr<Node>& a, const shared_ptr<Node>& b) {
        return (a->g + a->h) > (b->g + b->h); // Min-heap
    }};
    priority_queue<shared_ptr<Node>, vector<shared_ptr<Node>>, Compare> pq;
public:
    void push(shared_ptr<Node> node) override { pq.push(node); }
    shared_ptr<Node> pop() override { auto n = pq.top(); pq.pop(); return n; }
    bool empty() const override { return pq.empty(); }
};

// ====================== Generic Search Algorithm ======================
struct SearchResult {
    int nodes_expanded;
    int solution_length;
    double time_seconds;
    double avg_heuristic;
    int initial_heuristic;
};

template<typename OpenListT>
SearchResult genericGraphSearch(
    const PuzzleState& initial,
    Heuristic& heuristic,
    bool use_heuristic
) {
    OpenListT open;
    unordered_set<PuzzleState, PuzzleState::Hash> closed;
    SearchResult result{0, 0, 0, 0, 0};

    auto start_time = Clock::now();
    int initial_h = use_heuristic ? heuristic.calculate(initial) : 0;
    result.initial_heuristic = initial_h;

    open.push(make_shared<Node>(initial, 0, initial_h, Action::NONE, nullptr));

    while (!open.empty()) {
        auto current = open.pop();
        result.nodes_expanded++;

        if (current->state.tiles == array<int,9>{1,2,3,4,5,6,7,8,0}) {
            vector<Action> path;
            for (auto n = current; n->parent; n = n->parent) 
                path.push_back(n->action);
            result.solution_length = path.size();
            break;
        }

        if (closed.count(current->state)) continue;
        closed.insert(current->state);

        // Generate successors in order: UP, LEFT, RIGHT, DOWN
        const int moves[4][2] = {{-1,0}, {0,-1}, {0,1}, {1,0}};
        const Action actions[4] = {Action::UP, Action::LEFT, Action::RIGHT, Action::DOWN};

        for (int i = 0; i < 4; ++i) {
            int new_row = current->state.blank_pos/3 + moves[i][0];
            int new_col = current->state.blank_pos%3 + moves[i][1];
            
            if (new_row < 0 || new_row > 2 || new_col < 0 || new_col > 2) continue;
            
            int new_pos = new_row*3 + new_col;
            auto new_tiles = current->state.tiles;
            swap(new_tiles[current->state.blank_pos], new_tiles[new_pos]);
            
            PuzzleState new_state(new_tiles);
            if (current->parent && new_state == current->parent->state) continue;

            int h = use_heuristic ? heuristic.calculate(new_state) : 0;
            open.push(make_shared<Node>(
                new_state, current->g+1, h, actions[i], current
            ));
        }
    }

    result.time_seconds = chrono::duration<double>(Clock::now() - start_time).count();
    result.avg_heuristic = use_heuristic ? heuristic.average() : 0.0;
    return result;
}

// ====================== Main Program ======================
vector<array<int,9>> parseInput(const string& line) {
    vector<array<int,9>> puzzles;
    istringstream iss(line);
    string puzzle_str;
    
    while (getline(iss, puzzle_str, ',')) {
        array<int, 9> puzzle;
        istringstream tss(puzzle_str);
        for (int i = 0; i < 9; ++i) {
            if (!(tss >> puzzle[i])) {
                throw runtime_error("Invalid puzzle format");
            }
        }
        puzzles.push_back(puzzle);
    }
    return puzzles;
}

vector<array<int,9>> 


    

int main(int argc, char* argv[]) {
    if (argc < 3) {
        cerr << "Usage: " << argv[0] << " -alg puzzle_states..." << endl;
        return 1;
    }

    string alg = argv[1];
    string puzzle_line = argv[2];
    auto puzzles = parseInput(puzzle_line);
    
    //  Prints linearly the puzzles
    for (const auto& puzzle : puzzles) {
        for (int i = 0; i < 9; i++) {
            cout << puzzle[i] << " ";
            if ((i + 1) % 3 == 0) {
                cout << endl;
            }
        }
        cout << endl;
    }

    ManhattanHeuristic heuristic;
    SearchResult result;

    for (const auto& puzzle : puzzles) {
        try {
            if (alg == "-bfs") {
                result = genericGraphSearch<BFSOpenList>(
                    PuzzleState(puzzle), heuristic, false
                );
            }
            else if (alg == "-astar") {
                result = genericGraphSearch<AStarOpenList>(
                    PuzzleState(puzzle), heuristic, true
                );
            }
            else {
                throw invalid_argument("Unsupported algorithm");
            }

            cout << result.nodes_expanded << ","
                 << result.solution_length << ","
                 << result.time_seconds << ","
                 << result.avg_heuristic << ","
                 << result.initial_heuristic << endl;
                
        } catch (const exception& e) {
            cout << "-,-,-,-,-" << endl;
            cerr << "Error: " << e.what() << endl;
        }
    }
}