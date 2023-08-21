import numpy as np
import tkinter as tk
from tkinter import messagebox

class StartupScreen(tk.Tk):
    def __init__(self, main_app):
        super().__init__()

        self.main_app = main_app

        self.title("Select Difficulty")
        self.geometry("200x150")

        self.label = tk.Label(self, text="Choose Difficulty:")
        self.label.pack(pady=10)

        self.difficulty_var = tk.StringVar(self)
        self.difficulty_var.set("Medium")  

        choices = ["Easy", "Medium", "Hard"]  
        self.dropdown = tk.OptionMenu(self, self.difficulty_var, *choices)
        self.dropdown.pack(pady=10)

       
        self.start_button = tk.Button(self, text="Start Game", command=self.main_app.start_game)
        self.start_button.pack(pady=20)

    def get_difficulty(self):
        return self.difficulty_var.get()


class SudokuGame(tk.Tk):
    def __init__(self, sudoku_board, main_app):
        super().__init__()

        self.main_app = main_app

        self.title("Sudoku")
        self.geometry("270x270")
        self.board = np.array(sudoku_board)
        
        self.entries = []

        for i in range(9):
            row_entries = []
            for j in range(9):
                val = self.board[i, j]
                if val:
                    lbl = tk.Label(self, text=str(val), width=3, borderwidth=1, relief="solid")
                    lbl.grid(row=i, column=j)
                else:
                    e = tk.Entry(self, width=2, justify='center')
                    e.grid(row=i, column=j)
                    row_entries.append(e)
            self.entries.append(row_entries)

        btn = tk.Button(self, text="Check", command=self.check_solution)
        btn.grid(row=9, columnspan=9)

        self.solve_btn = tk.Button(self, text="Auto Solve", command=self.auto_solve)
        self.solve_btn.grid(row=10, columnspan=9)

    def check_solution(self):
        for i in range(9):
            for j in range(9):
                if not self.board[i, j]:
                    value = self.entries[i][j].get()
                    if value:
                        self.board[i, j] = int(value)
        if sudoku_grid_correct(self.board.tolist()):
            messagebox.showinfo("Success", "Correct solution!")
        else:
            messagebox.showwarning("Wrong", "Incorrect solution!")

    def solve(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True  
        row, col = empty

        for num in range(1, 10):
            if is_valid_move(board, num, (row, col)):
                board[row, col] = num
                if self.solve(board):  
                    return True  
                board[row, col] = 0  

        return False

    def find_empty(self, board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    return i, j  
        return None

    def auto_solve(self):
        board_copy = self.board.copy()
        if self.solve(board_copy):
            for i in range(9):
                for j in range(9):
                    if not self.board[i, j]:
                        self.entries[i][j].delete(0, tk.END)
                        self.entries[i][j].insert(0, str(board_copy[i, j]))
            messagebox.showinfo("Solved", "The Sudoku puzzle has been solved!")
        else:
            messagebox.showwarning("Error", "Unable to solve this puzzle!")


def generate_sudoku(difficulty="Medium"):
    if difficulty == "Easy":
        fill_factor = 0.6
        remove_factor = 0.2
    elif difficulty == "Hard":
        fill_factor = 0.3
        remove_factor = 0.5
    else:  
        fill_factor = 0.5
        remove_factor = 0.3

    
    sudoku = np.zeros((9, 9), dtype=int)

    for _ in range(int(81 * fill_factor)):
        row, col, num = np.random.randint(9), np.random.randint(9), np.random.randint(1, 10)
        while not is_valid_move(sudoku, num, (row, col)) or sudoku[row, col] != 0:
            row, col, num = np.random.randint(9), np.random.randint(9), np.random.randint(1, 10)
        sudoku[row, col] = num
    

    for _ in range(int(81 * remove_factor)):
        row, col = np.random.randint(9), np.random.randint(9)
        sudoku[row, col] = 0
    
    return sudoku

def is_valid_move(sudoku, num, position):

    row, col = position


    if num in sudoku[row, :]:
        return False


    if num in sudoku[:, col]:
        return False


    box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
    if num in sudoku[box_start_row:box_start_row+3, box_start_col:box_start_col+3]:
        return False

    return True

def row_correct(sudoku: np.ndarray, row_no: int) -> bool:
    row = sudoku[row_no]
    unique_non_zero = np.unique(row[row != 0])
    return len(unique_non_zero) == np.sum(row != 0)

def column_correct(sudoku: np.ndarray, column_no: int) -> bool:
    col = sudoku[:, column_no]
    unique_non_zero = np.unique(col[col != 0])
    return len(unique_non_zero) == np.sum(col != 0)

def block_correct(sudoku: np.ndarray, row_no: int, column_no: int) -> bool:
    block = sudoku[row_no:row_no + 3, column_no:column_no + 3]
    unique_non_zero = np.unique(block[block != 0])
    return len(unique_non_zero) == np.sum(block != 0)

def sudoku_grid_correct(sudoku: list) -> bool:
    sudoku = np.array(sudoku)
    for i in range(9):
        if not row_correct(sudoku, i) or not column_correct(sudoku, i):
            return False
    
    for i in [0, 3, 6]:
        for j in [0, 3, 6]:
            if not block_correct(sudoku, i, j):
                return False
                
    return True

if __name__ == "__main__":
    class MainApp:
        def __init__(self):
            self.startup_screen = StartupScreen(self)
            self.startup_screen.mainloop()

        def start_game(self):
            difficulty = self.startup_screen.get_difficulty()
            sudoku = generate_sudoku(difficulty)
            self.startup_screen.destroy()
            self.sudoku_app = SudokuGame(sudoku, self)
            self.sudoku_app.mainloop()

    app = MainApp()
