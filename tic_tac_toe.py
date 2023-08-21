import tkinter as tk
from tkinter import messagebox

class TicTacToe:

    def __init__(self):
        self.setup_main_window()
        self.initialize_game_state()
        self.create_display_widgets()
        self.arrange_widgets()

    def setup_main_window(self):
        """Initialize the main application window."""
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")

    def initialize_game_state(self):
        """Initialize game variables."""
        self.board = [""] * 9
        self.current_player = "X"

    def create_display_widgets(self):
        """Create GUI widgets."""
        self.turn_label = tk.Label(self.window, text=self.get_turn_text(), font='Arial 20')
        self.buttons = [
            tk.Button(self.window, text="", font='Arial 20', width=5, height=2, command=lambda i=i: self.make_move(i)) 
            for i in range(9)
        ]

    def arrange_widgets(self):
        """Position widgets in the main window."""
        self.turn_label.grid(row=0, columnspan=3)
        for idx, button in enumerate(self.buttons):
            row = (idx // 3) + 1
            col = idx % 3
            button.grid(row=row, column=col)

    def get_turn_text(self):
        """Return text indicating whose turn it is."""
        return f"Player {self.current_player}'s Turn"

    def make_move(self, position):
        """Update board, switch players, and check game status after a move."""
        if not self.board[position]:
            self.board[position] = self.current_player
            self.update_button(position)
            if self.has_winning_combination():
                self.display_winner(self.current_player)
                self.reset_game()
            elif "" not in self.board:
                self.display_winner("Tie")
                self.reset_game()
            else:
                self.toggle_player()

    def update_button(self, position):
        """Update the appearance of the button after a move."""
        color = "blue" if self.current_player == "X" else "red"
        self.buttons[position].config(text=self.current_player, fg=color)
        
    def has_winning_combination(self):
        """Return True if the current player has a winning combination."""
        combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        return any(all(self.board[i] == self.current_player for i in combo) for combo in combinations)

    def toggle_player(self):
        """Switch to the other player."""
        self.current_player = "O" if self.current_player == "X" else "X"
        self.turn_label.config(text=self.get_turn_text())

    def display_winner(self, winner):
        """Display the winner or if it's a tie."""
        message = "It's a Tie!" if winner == "Tie" else f"Player {winner} wins!"
        messagebox.showinfo("Tic Tac Toe", message)

    def reset_game(self):
        """Reset the game to its initial state."""
        self.initialize_game_state()
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL)
        self.turn_label.config(text=self.get_turn_text())

    def run(self):
        """Start the main loop of the GUI."""
        self.window.mainloop()

if __name__ == "__main__":
    TicTacToe().run()


'''
written by Thomas Tannenberg
21.08.2023
'''
