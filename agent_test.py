"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest
import random
import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)


if __name__ == '__main__':
#    unittest.main()
#DELETE BELOW


    from isolation import Board
    from game_agent import AlphaBetaPlayer
    from game_agent import MinimaxPlayer
    from sample_players import GreedyPlayer
    from sample_players import RandomPlayer

    from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)
    from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score,
                        custom_score_2, custom_score_3)

    # create an isolation board (by default 7x7)
    opponent  = AlphaBetaPlayer(score_fn=improved_score)
   
    #player2 = RandomPlayer()
    computer = AlphaBetaPlayer(score_fn=custom_score_2)

    
    game = Board(player_1=opponent, player_2=computer)
    move = random.choice(game.get_legal_moves())

    print(move,opponent,computer)
    
    game.apply_move(move)
    # place player 1 on the board at row 2, column 3, then place player 2 on
    # the board at row 0, column 5; display the resulting board state.  Note
    # that .apply_move() changes the calling object
    game.apply_move((0, 0))
    game.apply_move((1, 1))
    
    winner, history, outcome = game.play()
    print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
    print(game.to_string())
    
    print("Move history:\n{!s}".format(history))
    if winner==opponent:
        print("Opponent winner.")
    else:
        print("Computer winner.")
        
    
