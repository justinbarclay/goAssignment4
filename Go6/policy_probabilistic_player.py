#!/usr/bin/python3
from mcts import MCTS
from gtp_connection import GtpConnection
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='Process Arguments for number of simulation')
parser.add_argument('-s', '--sim', type=int, nargs='?', default = 200, help='define number of simulations for each legal move, #playout --> sim*num_of_legal_moves')
args = parser.parse_args()
num_simulation = args.sim

class Go6Player():
    def __init__(self, num_simulation = 200, limit=100, exploration = 0.01):
        """
        Player that selects a move based on MCTS from the set of legal moves

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """
        self.name = "MCTS Player"
        self.version = 0.1
        self.MCTS= MCTS()
        self.rate = 0.1
        self.num_simulation = num_simulation
        self.limit = limit
        self.exploration = exploration 
        
    def policy(self,board,color):
        return GoBoardUtil.generate_move_with_filter(board,pattern,check_selfatari)

    def run(self, board, color, print_info=False):
        self.MCTS.exploration = self.exploration
        self.MCTS.limit = self.limit
        self.MCTS.toplay = color
        self.MCTS.pattern = True
        self.MCTS.selfatari = True

        for n in range(self.num_simulation):
            board_copy = board.copy()
            self.MCTS._playout(board_copy, color)

        if print_info:
            self.MCTS.good_print(board, self.MCTS._root, color,self.num_nodes)
    
    def reset(self):
        self.MCTS = MCTS()

    def update(self, move):
        self.MCTS.update_with_move(move)

    def get_move(self, board, toplay):
        moves = GoBoardUtil.probabilistic_policy(board, toplay)
        verify_weights(moves)

        return random_select(moves)[0]

# Code given to us in prob_select.py
# downloaded from https://webdocs.cs.ualberta.ca/~mmueller/courses/496-Winter-2017/assignments/a4.html on April 8, 2017
# probabilities should add up to 1
def verify_weights(distribution):
    epsilon = 0.000000001 # allow small numerical error
    sum = 0.0
    for item in distribution:
        sum += item[1]
    assert abs(sum - 1.0) < epsilon

# This method is slow but simple
def random_select(distribution):
    r = random.random();
    sum = 0.0
    for item in distribution:
        sum += item[1]
        if sum > r:
            return item
    return distribution[-1] # some numerical error, return last element

if __name__=='__main__':
    c = GtpConnection(Go6Player(num_simulation))
    c.start_connection()

