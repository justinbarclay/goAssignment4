#!/usr/bin/python3

from board_util import GoBoardUtil
from gtp_connection import GtpConnection

class PolicyPlayer(object):
    """
        Plays according to the Go4 playout policy.
        No simulations, just random choice among current policy moves
    """

    version = 0.1
    name = "PolicyPlayer"
    def __init__(self):
        pass

    def get_move(self, board, toplay):
        moves = GoBoardUtil.probabilistic_policy(board, toplay)

        moves_with_max = []
        max_prob = moves[0][1]
        moves_with_max.append(moves[0][0])

        for move, val in moves:
            if val == max_prob:
                moves_with_max.append(move)
            else:
                break

        return sorted(moves_with_max, key=lambda x: x)[0]

    def get_properties(self):
        return dict(
            version=self.version,
            name=self.__class__.__name__,
        )

    def reset(self):
        return

def createPolicyPlayer():
    con = GtpConnection(PolicyPlayer())
    con.start_connection()

if __name__=='__main__':
    createPolicyPlayer()

