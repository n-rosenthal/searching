from sudoku.Board import SudokuBoard;
from copy import deepcopy

class GameState:
    """
    `GameState` represents the state of a Sudoku game.
    
    Attributes:
        board (SudokuBoard): The current state of the board
        moves (int): The number of moves made in the game
        history (list[SudokuBoard]): The history of moves made in the game
        parent (GameState): The parent state of the game
        
    Methods:
        get_neighbors(board: SudokuBoard) -> list[SudokuBoard]:
            Returns a list of possible neighbor states for the next empty position of the board.
        evaluate_state(board: SudokuBoard) -> int:
            Evaluates the current state of the board and returns a score. This is a wrapper for a custom evaluation function (heuristic function).
        
    """
    
    def __init__(self, board: SudokuBoard, moves: int = 0, history: list[SudokuBoard] = [], parent: "GameState" = None):
        self.board = board
        self.moves = moves
        self.history = history
        self.parent = parent
    
    def get_neighbors(self, board: SudokuBoard) -> list[SudokuBoard]:
        pos : tuple[int, int] = board.get_empty_cells()[0];
        print(pos);
        conflicts : list[int] = board.get_conflicts(pos[0], pos[1]);
        possible_values : set[int] = set(range(1, 10)) - set(conflicts);
        print(possible_values);
        neighbors : list[SudokuBoard] = [];
        for value in possible_values:
            new_board = deepcopy(board);
            new_board.set_value(pos[0], pos[1], value);
            neighbors.append(GameState(new_board, self.moves + 1, self.history + [board], self));
        return neighbors;
    
    def evaluate_state(self, board: SudokuBoard) -> int | float:
        """
        Evaluates a state of the game (that is, a sudoku board) and returns a score.
        
        Parameters:
            board (SudokuBoard): The board to evaluate.
        
        Returns:
            int | float: The score of the state.
        """
        return len(board.get_conflicting_cells());
    
b_1 : str = "\
5 3 0 0 7 0 5 0 3\n\
6 0 0 1 9 5 0 0 0\n\
0 9 8 0 0 0 0 6 0\n\
8 0 0 0 6 0 0 0 3\n\
4 0 0 8 0 3 0 0 1\n\
7 0 0 0 2 0 0 0 6\n\
0 6 0 0 0 0 2 8 0\n\
5 0 0 4 1 9 0 0 5\n\
0 0 0 0 8 0 0 7 9\n";