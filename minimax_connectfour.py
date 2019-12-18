""" Brandon Fonticoba
    October 2019
    AI - Dr. Burns
"""


import copy
import time
import abc
import random
import math


class Game(object):
    """A connect four game."""
    def __init__(self, grid):
        """Instances differ by their board."""
        self.grid = copy.deepcopy(grid)  # No aliasing!

    def display(self):
        """Print the game board."""
        for row in self.grid:
            for mark in row:
                print(mark, end='')
            print()
        print()

    def possible_moves(self):
        """Return a list of possible moves given the current board."""
        moves = []
        counter = 0

        while counter < 8:
            if self.grid[0][counter] == '-':  # if a column has an empty space at the top, that is a possible move.
                moves.append(counter)
            counter = counter + 1
        return moves

    def neighbor(self, col, color):
        """Return a Game instance like this one but with a move made into the specified column."""
        counter = 0
        new_grid = self.grid
        return_grid = Game(new_grid)

        while counter < 8:
            if self.grid[counter][col] == '-' and counter == 7:  # empty column insert at bottom.
                return_grid.grid[counter][col] = color
                break
            elif self.grid[counter][col] == '-':  # keep checking for the lowest possible spot in column.
                counter = counter + 1
            else:  # found another piece so insert new piece above in the column, or row - 1
                return_grid.grid[counter - 1][col] = color
                break

        return return_grid

    def utility(self):
        """Return the minimax utility value of this game"""
        value = 0

        # Vertical
        for col in range(8):  # looking through all the columns.
            col_list = [self.grid[i][col] for i in range(8)]  # grab each column of pieces to check for score values.
            for row in range(8 - 3):
                four_piece = col_list[row:row + 4]  # looking at four pieces at a time to give a score to.
                value += self.four_score(four_piece)

        # Horizontal
        for row in range(8):  # looking through all the rows
            row_list = [i for i in list(self.grid[row])]  # grab each row of pieces to check for score values.
            for col in range(8-3):
                four_piece = row_list[col:col+4]  # looking at four pieces at a time to give a score to.
                value += self.four_score(four_piece)

        # Negative Diagonal
        for row in range(8 - 3):  # looking through all the negative diagonals.
            for col in range(8 - 3):
                four_piece = [self.grid[row + 3 - i][col + i] for i in range(4)]  # looking at four pieces at a time to give a score to.
                value += self.four_score(four_piece)

        # Positive Diagonal
        for row in range(8-3):  # looking through all positive diagonals.
            for col in range(8-3):
                four_piece = [self.grid[row+i][col+i] for i in range(4)]  # looking at four pieces at a time to give a score to.
                value += self.four_score(four_piece)

        # Center Column Score
        center_column1 = [self.grid[i][3] for i in range(8)]
        count_pieces = center_column1.count('R')
        value += count_pieces * 2

        # Center Column Score
        center_column2 = [self.grid[i][4] for i in range(8)]
        count_pieces2 = center_column2.count('R')
        value += count_pieces2 * 2

        return value

    def four_score(self, four_piece):
        # Not seven years ago, but gives a score to the 4 slots on the grid being examined.
        score = 0

        if four_piece.count('R') == 4:  # if their are four red pieces in a row return a high value.
            score += 100
        elif four_piece.count('R') == 3 and four_piece.count('-') == 1:  # if their are 3 red pieces in the four slots.
            score += 15
        elif four_piece.count('R') == 2 and four_piece.count('-') == 2:  # if their are 2 red pieces in the four slots.
            score += 5
        elif four_piece.count('B') == 3 and four_piece.count('R') == 1:  # if the other player (Black) has 3 pieces in the four slots.
            score += 200

        return score

    def winning_state(self):
        """Returns float("inf") if Red wins; float("-inf") if Black wins;
           0 if board full; None if not full and no winner"""
        red_win = float("inf")
        black_win = float("-inf")
        board_full = 0

        moves = self.possible_moves()
        if len(moves) == 0:
            return board_full

        # Vertical
        for col in range(8):
            for row in range(8 - 3):
                if self.grid[row][col] == 'R' and self.grid[row + 1][col] == 'R' and self.grid[row + 2][col] == 'R' and self.grid[row + 3][col] == 'R':
                    return red_win
                elif self.grid[row][col] == 'B' and self.grid[row + 1][col] == 'B' and self.grid[row + 2][col] == 'B' and self.grid[row + 3][col] == 'B':
                    return black_win

        # Horizontal
        for col in range(8-3):
            for row in range(8):
                if self.grid[row][col] == 'R' and self.grid[row][col+1] == 'R' and self.grid[row][col+2] == 'R' and self.grid[row][col+3] == 'R':
                    return red_win
                elif self.grid[row][col] == 'B' and self.grid[row][col+1] == 'B' and self.grid[row][col+2] == 'B' and self.grid[row][col+3] == 'B':
                    return black_win

        # Negative Diagonal
        for col in range(8-3):
            for row in range(3, 8):
                if self.grid[row][col] == 'R' and self.grid[row-1][col+1] == 'R' and self.grid[row-2][col+2] == 'R' and self.grid[row-3][col+3] == 'R':
                    return red_win
                elif self.grid[row][col] == 'B' and self.grid[row-1][col+1] == 'B' and self.grid[row-2][col+2] == 'B' and self.grid[row-3][col+3] == 'B':
                    return black_win

        # Positive Diagonal
        for col in range(8 - 3):
            for row in range(8 - 3):
                if self.grid[row][col] == 'R' and self.grid[row + 1][col + 1] == 'R' and self.grid[row + 2][col + 2] == 'R' and self.grid[row + 3][col + 3] == 'R':
                    return red_win
                elif self.grid[row][col] == 'B' and self.grid[row + 1][col + 1] == 'B' and self.grid[row + 2][col + 2] == 'B' and self.grid[row + 3][col + 3] == 'B':
                    return black_win


class Agent(object):
    """Abstract class, extended by classes RandomAgent, FirstMoveAgent, MinimaxAgent.
    Do not make an instance of this class."""

    def __init__(self, color):
        """Agents use either RED or BLACK chips."""
        self.color = color

    @abc.abstractmethod
    def move(self, game):
        """Abstract. Must be implemented by a class that extends Agent."""
        pass


class RandomAgent(Agent):
    """Naive agent -- always performs a random move"""

    def move(self, game):
        """Returns a random move"""
        # agent picks a random column to drop in each time.
        while 1:
            col = random.randrange(0, 8)
            if game.grid[0][col] == '-':
                return col


class FirstMoveAgent(Agent):
    """Naive agent -- always performs the first move"""

    def move(self, game):
        """Returns the first possible move"""
        # agent always picks the first available column to drop in each time.
        moves = game.possible_moves()
        return moves[0]


class MinimaxAgent(Agent):
    """Smart agent -- uses minimax to determine the best move"""

    def move(self, game):
        """Returns the best move using minimax"""
        # getting the column (col) and minimax score (score) for the current game state looking two moves ahead, that is what the 2 represents.
        col, score = self.minimax(game, 2, -math.inf, math.inf, True)
        return col

    # minimax algorithm
    def minimax(self, game, depth, alpha, beta, max_player):
        if depth == 0:
            return None, game.utility()  # when reaching the max depth for the search return only the score of that state.

        if max_player:  # minimax agent
            max_value = -math.inf  # max score for each state
            column = 0  # column where highest score comes from
            for col in game.possible_moves():
                value = MinimaxAgent.minimax(self, (game.neighbor(col, 'R')), depth-1, alpha, beta, False)[1]  # recursive call switching to random agent.
                if value > max_value:
                    max_value = value
                    column = col
                alpha = max(alpha, max_value)
                if alpha >= beta:
                    break
            return column, max_value  # returning both the column and the score.

        else:  # random agent
            min_value = math.inf  # min score for each state
            column = 0  # column where lowest score comes from
            for col in game.possible_moves():
                value = MinimaxAgent.minimax(self, (game.neighbor(col, 'B')), depth - 1, alpha, beta, True)[1] # recursive call switching to minimax agent.
                if value < min_value:
                    min_value = value
                    column = col
                beta = min(beta, min_value)
                if alpha >= beta:
                    break
            return column, min_value  # returning both the column and the score.


def tournament(simulations=50):
    """Simulate connect four games, of a minimax agent playing
    against a random agent"""

    redwin, blackwin, tie = 0,0,0
    for i in range(simulations):

        game = single_game(io=False)

        print(i, end=" ")
        if game.winning_state() == float("inf"):
            redwin += 1
        elif game.winning_state() == float("-inf"):
            blackwin += 1
        elif game.winning_state() == 0:
            tie += 1

    print("Red %d (%.0f%%) Black %d (%.0f%%) Tie %d" % (redwin,redwin/simulations*100,blackwin,blackwin/simulations*100,tie))

    return redwin/simulations


def single_game(io=True):
    """Create a game and have two agents play it."""

    game = Game([['-' for i in range(8)] for j in range(8)])   # 8x8 empty board
    if io:
        game.display()

    # maxplayer = FirstMoveAgent('R')
    # minplayer = MinimaxAgent('B')

    # maxplayer = MinimaxAgent('R')
    # minplayer = FirstMoveAgent('B')

    maxplayer = MinimaxAgent('R')
    minplayer = RandomAgent('B')

    # maxplayer = RandomAgent('R')
    # minplayer = MinimaxAgent('B')


    while True:

        m = maxplayer.move(game)
        game = game.neighbor(m, maxplayer.color)
        if io:
            time.sleep(1)
            game.display()

        if game.winning_state() is not None:
            break

        m = minplayer.move(game)
        game = game.neighbor(m, minplayer.color)
        if io:
            # time.sleep(1)
            game.display()

        if game.winning_state() is not None:
            break

    if game.winning_state() == float("inf"):
        print("RED WINS!")
    elif game.winning_state() == float("-inf"):
        print("BLACK WINS!")
    elif game.winning_state() == 0:
        print("TIE!")

    return game


if __name__ == '__main__':
    # single_game(io=True)
    tournament(simulations=50)
