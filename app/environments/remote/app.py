# Adapted from https://mblogscode.com/2016/06/03/python-naughts-crossestic-tac-toe-coding-unbeatable-ai/

from flask import Flask, request
from uuid import uuid4
import sys
import traceback


app = Flask(__name__)
games = {} # mapping of game_id => TicTacToeGame


@app.errorhandler(500)
def internal_error(exception):
    print("500 error caught")
    etype, value, tb = sys.exc_info()
    print(traceback.print_exception(etype, value, tb))


@app.route("/newgame")
def newgame():
    id = str(uuid4())
    game = TicTacToeGame()
    games[id] = game
    response = {
        "id": id,
        "player_count": 2,
        "action_space_size": 9,
        "observation_space_size": 9,
        "current_player": 0,
        "observation": game.observation,
        "legal_actions": game.legal_actions,
    }
    return response


@app.route("/step/<string:id>", methods=["POST"])
def step(id):
    data = request.get_json(force=True)
    action = data['action']
    game = games[id]
    observation, reward, done, _ = game.step(action)

    return {
        "next_player": game.current_player_num,
        "observation": observation,
        "legal_actions": game.legal_actions,
        "reward": reward,
        "done": done
    }


@app.route("/render/<string:id>")
def render(id):
    game = games[id]
    return {
        "output": game.render()
    }


class Player():
    def __init__(self, id, token):
        self.id = id
        self.token = token


class Token():
    def __init__(self, symbol, number):
        self.number = number
        self.symbol = symbol


class TicTacToeGame:
    def __init__(self):
        self.name = 'tictactoe'
        self.grid_length = 3
        self.n_players = 2
        self.num_squares = self.grid_length * self.grid_length
        self.board = [Token('.', 0)] * self.num_squares
        self.players = [Player('1', Token('X', 1)), Player('2', Token('O', -1))]
        self.current_player_num = 0
        self.turns_taken = 0
        self.done = False
        self.verbose = True

    @property
    def observation(self):
        if self.players[self.current_player_num].token.number == 1:
            position = [x.number for x in self.board]
        else:
            position = [-x.number for x in self.board]

        la_grid = self.legal_actions
        position.extend(la_grid)
        return position

    @property
    def legal_actions(self):
        legal_actions = []
        for action_num in range(len(self.board)):
            if self.board[action_num].number == 0: #empty square
                legal_actions.append(1)
            else:
                legal_actions.append(0)
        return legal_actions

    def square_is_player(self, square, player):
        return self.board[square].number == self.players[player].token.number

    def check_game_over(self):
        board = self.board
        current_player_num = self.current_player_num
        players = self.players

        # check game over
        for i in range(self.grid_length):
            # horizontals and verticals
            if ((self.square_is_player(i*self.grid_length,current_player_num) and self.square_is_player(i*self.grid_length+1,current_player_num) and self.square_is_player(i*self.grid_length+2,current_player_num))
                or (self.square_is_player(i+0,current_player_num) and self.square_is_player(i+self.grid_length,current_player_num) and self.square_is_player(i+self.grid_length*2,current_player_num))):
                return  1, True

        # diagonals
        if((self.square_is_player(0,current_player_num) and self.square_is_player(4,current_player_num) and self.square_is_player(8,current_player_num))
            or (self.square_is_player(2,current_player_num) and self.square_is_player(4,current_player_num) and self.square_is_player(6,current_player_num))):
                return  1, True

        if self.turns_taken == self.num_squares:
            return  0, True

        return 0, False

    @property
    def current_player(self):
        return self.players[self.current_player_num]

    def step(self, action):
        reward = [0,0]

        # check move legality
        board = self.board

        if (board[action].number != 0):  # not empty
            done = True
            reward = [1, 1]
            reward[self.current_player_num] = -1
        else:
            board[action] = self.current_player.token
            self.turns_taken += 1
            r, done = self.check_game_over()
            reward = [-r,-r]
            reward[self.current_player_num] = r

        self.done = done

        if not done:
            self.current_player_num = (self.current_player_num + 1) % 2

        return self.observation, reward, done, {}

    def render(self):
        response = ""
        if self.done:
            response = f'GAME OVER'
        else:
            response = f"It is Player {self.current_player.id}'s turn to move\n"

        response += '\n'.join([x.symbol for x in self.board[:self.grid_length]])
        response += '\n'.join([x.symbol for x in self.board[self.grid_length:self.grid_length*2]])
        response += '\n'.join([x.symbol for x in self.board[(self.grid_length*2):(self.grid_length*3)]])

        if self.verbose:
            response += f'\nObservation: \n{self.observation}'

        if not self.done:
            response += f'\nLegal actions: {[i for i,o in enumerate(self.legal_actions) if o != 0]}'

        return response


def checkWin(b, m):
    return ((b[0] == m and b[1] == m and b[2] == m) or  # H top
            (b[3] == m and b[4] == m and b[5] == m) or  # H mid
            (b[6] == m and b[7] == m and b[8] == m) or  # H bot
            (b[0] == m and b[3] == m and b[6] == m) or  # V left
            (b[1] == m and b[4] == m and b[7] == m) or  # V centre
            (b[2] == m and b[5] == m and b[8] == m) or  # V right
            (b[0] == m and b[4] == m and b[8] == m) or  # LR diag
            (b[2] == m and b[4] == m and b[6] == m))  # RL diag


def checkDraw(b):
    return 0 not in b

def getBoardCopy(b):
    # Make a duplicate of the board. When testing moves we don't want to
    # change the actual board
    dupeBoard = []
    for j in b:
        dupeBoard.append(j)
    return dupeBoard

def testWinMove(b, mark, i):
    # b = the board
    # mark = 0 or X
    # i = the square to check if makes a win
    bCopy = getBoardCopy(b)
    bCopy[i] = mark
    return checkWin(bCopy, mark)


def testForkMove(b, mark, i):
    # Determines if a move opens up a fork
    bCopy = getBoardCopy(b)
    bCopy[i] = mark
    winningMoves = 0
    for j in range(0, 9):
        if testWinMove(bCopy, mark, j) and bCopy[j] == 0:
            winningMoves += 1
    return winningMoves >= 2
