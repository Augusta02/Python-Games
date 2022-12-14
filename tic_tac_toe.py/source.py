import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

# Define Classes for the Players and Their Moves
# define Player class
# .label atrribute should store player signs, X and o
#  .color attribute should hold a string with a Tkinter color
class Player(NamedTuple):
    # changed the : to =
    label :str
    color :str

# define Move class
class Move(NamedTuple):
    #  .row and .col attributes should 
    # hold the coordinates that identify the move's target cell
    # changed the : to =
    row:int
    col : int
    # label defaults to empty string 
    # meaning the move has not been playe yet
    label: str= ""


# define the constants
BOARD_SIZE= 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color= "green"),
)

# Create a class to represent the Game Logic
class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves =[]
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    # setup abstract Game board
    # _setup_board() method inital vales for _current_moves and _winning_moves
    def _setup_board(self):
        self._current_moves = [
            [Move(row,col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos= self._get_winning_combos()

    # create the winning combos
    def _get_winning_combos(self):
        rows=[
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns= [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal= [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    # validate player's move
    # is._valid_move() takes a move object as a n argument
    def is_valid_move(self, move):
        '''Return True if move is valid, and False otherwise'''
        # .row and .col coordinates from the input move
        row, col = move.row, move.col
        # rhis would check if [row] [col] still holds an empty string as label
        # condition will be True if no player
        # has made the input move
        move_was_not_played = self._current_moves[row][col].label == ""
        # checks if the game doesnt have a winner yet
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    # process players moves to find a winner
    def process_move(self, move):
        '''Process the current move and check if its a winning combo'''
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(
                self._current_moves[n][m].label
                for n, m in combo
            )
            is_win= (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break
    
    # checks if we have a winner
    def has_winner(self):
        '''Return True if the game has a winner, and False otherwise'''
        return self._has_winner

    # check for tied games
    def is_tied(self):
        '''Return True if the game is tied, and False otherwise'''
        no_winner = not self._has_winner
        played_moves= (
            move.label for row in self._current_moves for move in row  
        )
        return no_winner and all(played_moves)

    # toggle players between turns
    def toggle_player(self):
        '''Return a toggled player.'''
        self.current_player= next(self._players)
    
    # implement play again option
    def reset_game(self):
        """Reset the game state to play again"""
        # for loop sets all the current moves to an empty Move object
        for row , row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        
        self._has_winner = False
        self.winner_combo = []





    
# Create a class to represent the Game Board
# process players moves on the game board
class TicTacToeBoard(tk.Tk):
    # add game arguement to initializer
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac_Toe Game")
        self.__cells = {}
        # assign the argument to an instance attribute
        self._game = game 
        # add main menu to game's main window
        self._create_menu()
        # adds the display and grid of cells
        self._create_board_display()
        self._create_board_grid()

    # Option to play again and exit game
    # create and add main menu to game
    # define helper method _create_menu() to handle menu creation in one place
    def _create_menu(self):
        # create Menu instance, this would work as a menu bar
        menu_bar = tk.Menu(master=self)
        # sets menu bar object as the main menu of current Tkinter window
        self.config(menu=menu_bar)
        # create another Menu instance to provide a File menu
        # master arguemnt should be set to menu bar object
        file_menu = tk.Menu(master=menu_bar)
        # add meu option to File menu using the add_commond method
        # label should be "Play Option"
        # when player clicks on the said option
        # application should run the reset_board in the command arguement
        file_menu.add_command(label= "Play Again", command= self.reset_board)
        # add menu seperator
        # seperator is used to separate groups of relaated commands in a given dropdown menu
        file_menu.add_separator()
        # add exit command
        # application would run quit in the command arguement 
        file_menu.add_command(label="Exit", command=quit)
        # add file menu to menu bar by calling add_cascade()
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text= "Ready?",
            font= font.Font(size=28, weight="bold"),
        )
        self.display.pack()

# create grid cells using button objects
    def _create_board_grid(self):
        grid_frame= tk.Frame(master=self)
        grid_frame.pack()
        #._game which will give you full access to the game logic
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            # ._game.board_size to set the board size
            for col in range(self._game.board_size):
                button= tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self.__cells[button] =(row, col)
                # this binds the click event of every button on the game
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

    def play(self, event):
        '''Handle a players move'''
        clicked_btn = event.widget
        row, col = self.__cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg= f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)
    
    # update the game board to reflect the game state
    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self.__cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    # lets implement play again option
    def reset_board(self):
        '''Reset the game's board to play again'''
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self.__cells.keys():
            button.config(highlightbackground='lightblue')
            button.config(text="")
            button.config(fg="black")

# this helps displays the Tkinter app

def main():
    '''Create the game's board and run its main loop.'''
    game= TicTacToeGame()
    board= TicTacToeBoard(game)
    board.mainloop()

if __name__== "__main__":
    main()




