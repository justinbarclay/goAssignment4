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
        moves = GoBoardUtil.generate_move_with_filter(board, True, True)
        verify_weights(moves)
        
        return random_select(moves) 

    def get_properties(self):
        return dict(
            version=self.version,
            name=self.__class__.__name__,
        )
    def reset(self):
        pass

def createPolicyPlayer():
    con = GtpConnection(PolicyPlayer())
    con.start_connection()

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
    createPolicyPlayer()
