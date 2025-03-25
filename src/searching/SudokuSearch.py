""" src/searching/SudokuSearch.py
Implementation of local search algorithms for the Sudoku game.
Methods:
    -   random_walk
        Local search where the next state is chosen randomly from the neighbors of the current state.
"""

import  random;
from    sudoku.GameState    import GameState, SudokuBoard as Board;
from    sudoku.Board        import b_1, solved_board;

def random_walk(board: Board, niter: int = 1000) -> GameState:
    """
    Local Search where the next state is chosen randomly from the neighbors of the current state.
    
    Parameters:
        board (Board): The current state of the game.
        niter (int): The maximum number of iterations.
    
    Returns:
        GameState: The final state of the game.
    """
    #   Initialize the state
    state       : GameState         = GameState(board);
    visited     : set[GameState]    = set();
    frontier    : list[GameState]   = [state];
    
    #   Add the initial state to the visited set
    visited.add(state);
    
    #   Add the initial state to the frontier
    frontier.append(state);
    
    #   Local search with random walk as next state
    for i in range(niter):
        #   Is solved?
        if state.board.is_solved():
            print("Solved!");
            print(state.board.grid);
            break;
        
        #   Check if the frontier is empty
        if len(frontier) == 0:
            print("Frontier is empty");
            break;
        
        #   Get a random state from the frontier
        state = random.choice(frontier);
        
        #   Get the neighbors of the state
        neighbors = state.get_neighbors(state.board);
        
        #   Remove the state from the frontier
        frontier.remove(state);
        
        #   Add the neighbors to the frontier
        for neighbor in neighbors:
            if neighbor not in visited:
                frontier.append(neighbor);
                visited.add(neighbor);
        
        if i % 100 == 0:
            print("Iteration: ", i);
        
    #   Return the final state
    print(f"Iterations: {i}");
    return state;

if __name__ == "__main__":
    #   Solved board for testing
    board = Board.from_string(solved_board);
    state = random_walk(board, niter=1000);
    print(state.board.grid);
    
    #   Random board for testing
    board = Board.from_string(b_1);
    state = random_walk(board, niter=1000);
    print(state.board.grid);