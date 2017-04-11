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

        for move, val in moves:
            if val == max_prob:
                moves_with_max.append((move,val))
            else:
                break
        
        alphaList = []
        for move, val in moves_with_max:
            alphaList.append((board.point_to_string(move), move))

        return sorted(alphaList, key=lambda x: x[0])[0][1]

    def get_properties(self):
        return dict(
            version=self.version,
            name=self.__class__.__name__,
        )

    def update(self, move):
        pass

    def reset(self):
        pass
        
def createPolicyPlayer():
    con = GtpConnection(PolicyPlayer())
    con.start_connection()

if __name__=='__main__':
    createPolicyPlayer()

