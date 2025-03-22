"""
    src/searching/sudoku/Board.py
    Definition of the Sudoku board class.
"""

import numpy as np; 

#   Pre-defined boards
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

class SudokuBoard:
    """
    A `SudokuBoard` representation state.
    
    Attributes:
        grid (np.ndarray): 9x9 NumPy array of values
        fixed (np.ndarray): 9x9 NumPy array of booleans
        
    Methods:
        Validation of the board
            is_row_valid(row_index: int) -> bool
            is_valid() -> bool
            is_solved() -> bool
        
        Counting of conflicts
            get_conflicting_cells() -> list[tuple[int, int]]
        
        Getters
            get_value(row: int, col: int) -> int
            get_row(row_idx: int) -> np.ndarray
            get_col(col_idx: int) -> np.ndarray
            get_box(box_idx: int) -> np.ndarray
            get_empty_cells() -> list[tuple[int, int]]
        
        Setter
            set_value(row: int, col: int, value: int)
        
        Static initializers
            from_string(board_str: str)
            from_file(file_path: str)
        
    """
    def __init__(self, grid: np.ndarray | list[int], fixed: np.ndarray | list[bool]):
        """
        Given a 9x9 `grid` of integers and a 9x9 `fixed` array of booleans,
        creates a new `SudokuBoard` instance.
        
        Parameters:
            grid (np.ndarray | list[int]): 9x9 NumPy array of values
            fixed (np.ndarray | list[bool]): 9x9 NumPy array of booleans
            
        Raises:
            ValueError: If `grid` and `fixed` are not 9x9 NumPy arrays
        """
        if isinstance(grid, list): grid = np.array(grid);
        if isinstance(fixed, list): fixed = np.array(fixed);
        if grid.shape != (9, 9) or fixed.shape != (9, 9):
            raise ValueError("Grid and fixed must be 9x9 NumPy arrays");
        self.grid = grid;
        self.fixed = fixed;
    
    def is_row_valid(self, row_index: int) -> bool:
        """
        Returns True if the row at `row_index` is valid, and False otherwise.
        
        A row is valid if all non-zero values in the row are unique.
        """
        row = self.grid[row_index]
        seen = set()
        for val in row:
            if val != 0:
                if val in seen:
                    return False
                seen.add(val)
        return True
    
    def get_conflicting_cells(self) -> list[tuple[int, int]]:
        """
        Returns a list of cells which are in conflict. A conflict occurs when two or more cells in the same row, column, or box have the same value.
        
        The list of conflicts is returned as a list of tuples. Each tuple contains a pair of coordinates (row, column) which correspond to cells which are in conflict.
        """
        conflicts = set()
        # Check rows
        for i in range(9):
            seen = {}
            for j in range(9):
                val = self.grid[i][j]
                if val == 0:
                    continue
                if val in seen:
                    conflicts.update({(i, j), (i, seen[val])})
                else:
                    seen[val] = j
        # Check columns and boxes similarly...
        return list(conflicts)
    
    @classmethod
    def from_string(cls, board_str: str) -> "SudokuBoard":
        """
        Given a string representation of a Sudoku board, creates a new `SudokuBoard` instance.
        
        Parameters:
            board_str (str): A string representation of a Sudoku board.
            
        Returns:
            SudokuBoard: A new `SudokuBoard` instance.
        """
        board_str = board_str.replace(" ", "").replace("\n", "")
        grid = np.array([int(board_str[i * 9 + j]) for i in range(9) for j in range(9)]).reshape(9, 9)
        fixed = (grid != 0);
        print(grid)
        print(fixed)
        return cls(grid, fixed)

    def set_value(self, row: int, col: int, value: int) -> None:
        """
        Sets the value of a cell in the board.
        
        Parameters:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            value (int): The value to set the cell to.
        """
        if not self.fixed[row][col]:
            self.grid[row][col] = value
        else:
            raise ValueError("Cannot modify fixed cell")

    def get_row(self, row_idx: int) -> np.ndarray:
        """
        Returns a row of the Sudoku board as a numpy array.
        Parameters:
            row_idx (int): The index of the row to retrieve.
        Returns:
            np.ndarray: The row of the Sudoku board.
        """
        return self.grid[row_idx, :]

    def get_column(self, col_idx: int) -> np.ndarray:
        """
        Returns a column of the Sudoku board as a numpy array.
        
        Parameters:
            col_idx (int): The index of the column to retrieve.
        Returns:
            np.ndarray: The column of the Sudoku board.
        """
        return self.grid[:, col_idx]

    def get_box(self, box_idx: int) -> np.ndarray:
        """
        Returns a box (3x3 sub-matrix) of the Sudoku board as a numpy array.
        
        Parameters:
            box_idx (int): The index of the box to retrieve.
        Returns:
            np.ndarray: The box of the Sudoku board.
        """
        start_row = (box_idx // 3) * 3
        start_col = (box_idx % 3) * 3
        return self.grid[start_row:start_row+3, start_col:start_col+3].flatten()

    def get_empty_cells(self) -> list[tuple[int, int]]:
        """
        Returns a list of empty cells in the board.
        A cell is considered empty if its value is 0.
        
        Returns:
            list[tuple[int, int]]: A list of tuples representing the coordinates of the empty cells.
        """
        return [(i, j) for i in range(9) for j in range(9) if self.grid[i][j] == 0];
    
    def get_conflicts(self, row: int, col: int) -> set[int]:
        """
        Returns a set of values that conflict with the value at the given row and column.
        A conflict occurs when two or more cells in the same row, column, or box have the same value.
        
        Parameters:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
        
        Returns:
            set[int]: A set of values that conflict with the value at the given row and column.
        """
        row, col, box = self.get_row(row), self.get_column(col), self.get_box((row // 3) * 3 + (col // 3));
        return set(row[row != 0]) | set(col[col != 0]) | set(box[box != 0]);