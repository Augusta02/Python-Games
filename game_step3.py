import tkinter as tk
from itertools import cycle
from tkinter import font
from tkinter.tix import ComboBox
from typing import NamedTuple

class TicTacToeGame:

    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise"""
        row, col= move.row, move.col
        move_was_not_played = self._current_moves[row][col]
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        """Process the current move and check if its a win."""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(
                self._current_moves[n][m].label
                for n, m in combo
            )
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break


        def has_winner(self):
            """Return True if has game has a winner, and False otherwise"""
            return self._has_winner

        def is_tied(self):
            '''Return True if the game is tied, and False otherwise'''
            no_winner = not self._has_winner
            played_moves = (
                move.label for row in self._current_moves for move in row
            )
            return no_winner and all(played_moves)

        
        def toggle_player(self):
            '''Return a toggled player.'''
            self.current_player = next(self._players)



class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_board_display()
        self._create_board_grid()


    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):