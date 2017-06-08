"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """


    
    #   24 April 2017 Bhinesh Patel - Heuristic based on a prioritizing distance to the center
    #   and minimizing opponents available moves
    


    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player): 
        return float("inf")

    return -10*distance_from_center(game,player) + 10*ratio_heuristic(game,player)


def percent_full(game):
    #   return percent of board that is full
    return int(100*(1.0 - float(len(game.get_blank_spaces()))/(game.width*game.height)))
    
    
def ratio_heuristic(game,player):

    #   24-April-2017 Bhinesh Patel - Prefers move that reduces opponents moves. (Own Moves/Opponent Moves).     
    
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    if own_moves < 1:
        return float("-inf")
    if opp_moves < 1:
        return float("inf")

       
    if own_moves>opp_moves:
        return float(own_moves) / float(opp_moves)
    else:
        return float(-opp_moves) / float(own_moves)


def distance_from_player(game,player_1,player_2):
#   Return distance between two players
    y_1, x_1 = game.get_player_location(player_1)
    y_2, x_2 = game.get_player_location(player_2)
    return float((y_1 - y_2)**2 + (x_1 - x_2)**2)**0.5

def distance_from_center(game,player):
#   Return distance from center for player
    w, h = game.width, game.height
    y, x = game.get_player_location(player)
    return float(((h-1.0)/2.0 - y)**2 + ((w-1.0)/2.0 - x)**2)**0.5

def player_at_edge(game,player):
    #   return True/False if player is at edge of board

    w, h = game.width, game.height
    y, x = game.get_player_location(player)

    return (x in [0,w-1] or y in [0,h-1])

def center_heuristic(game,player):
    
    w, h = game.width, game.height
    y, x = game.get_player_location(player)
    oy,ox= game.get_player_location(game.get_opponent(player))
    #return 1.0 -((float((h/2.0 - y)**2 + (w/2.0 - x)**2))**0.5)/((float(h/2.0)**2 + float(w/2.0)**2)**0.5 )

    return float((h/2.0 - y)**2 + (w/2.0 - x)**2)**0.5

    
def space_heuristic(game,player):

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)

def manhattan_distance(game,player):
    y, x = game.get_player_location(player)
    oy,ox= game.get_player_location(game.get_opponent(player))

    return abs(y-oy)+abs(x-ox)

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    #   24 April 2017 Bhinesh Patel - Heuristic based on avoiding edge

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return 10.0*ratio_heuristic(game,player)

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player): 
        return float("inf")
   
    return -10*distance_from_center(game,player) 


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        #   If no legal moves left then return (-1,-1)...illegal move
        if not legal_moves:
            return (-1,-1)
        #   Get best_move
        else:
            #   5/8/2017 Re-Coded to make better use of memory as per suggestion by Udacity reviewer.
            #_,best_move = max([(self.min_value(game.forecast_move(m),depth-1),m) for m in legal_moves])
            max_score = float("-inf")
            best_move = legal_moves[0]
            for m in legal_moves:
                score = self.min_value(game.forecast_move(m),depth-1)
                if score > max_score:
                    max_score = score
                    best_move = m
                    
            return best_move


    def max_value(self,game,depth):
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #   Start Terminal Test               
        if depth < 1:
            return self.score(game,self)

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return self.score(game,self)
        #   End Terminal Test

        
        score = float("-inf")              
        for m in legal_moves:
            score = max(score,self.min_value(game.forecast_move(m),depth-1))
        return score
                
    def min_value(self,game,depth):
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #   Start Terminal Test               
        if depth < 1:
            return self.score(game,self)

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return self.score(game,self)
        #   End Terminal Test

        score = float("inf")               
        for m in legal_moves:
            score = min(score,self.max_value(game.forecast_move(m),depth-1))
        return score
        
class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            
            depth = 0
            while True:
                best_move=self.alphabeta(game, depth)
                depth += 1
               
             

        except SearchTimeout:
            return best_move  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

 
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1,-1)
        

        v = float("-inf")
        
        #   24 April 2017 Bhinesh Patel - Fails Udacity Test
        #   random.shuffle(legal_moves)
        #

        best_move=legal_moves[0]
        for m in legal_moves:
            t=self.ab_min_value(game.forecast_move(m),depth-1,alpha,beta)
            if t>v:
                v=t
                best_move=m
            
            if v >= beta:
                return m
            alpha=max(alpha,v)

        return best_move
        

    def ab_max_value(self,game,depth,alpha,beta):
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #   Start Terminal Test               
        if depth < 1:
            return self.score(game,self)

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return self.score(game,self)
        #   End Terminal Test
        
        v = float("-inf")
        
        #   24 April 2017 Bhinesh Patel - Fails Udacity Test
        #   random.shuffle(legal_moves)
        #
        for m in legal_moves:
            v = max(v,self.ab_min_value(game.forecast_move(m),depth-1,alpha,beta))
            if v >= beta:
                return v
            alpha=max(alpha,v)
        return v
            
                
    def ab_min_value(self,game,depth,alpha,beta):
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #   Start Terminal Test               
        if depth < 1:
            return self.score(game,self)

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return self.score(game,self)
        #   End Terminal Test
        
        v = float("inf")
        
        #   24 April 2017 Bhinesh Patel - Fails Udacity Test
        #   random.shuffle(legal_moves)
        #

        for m in legal_moves:
            v = min(v,self.ab_max_value(game.forecast_move(m),depth-1,alpha,beta))
            if v <= alpha:
                return v
            beta=min(beta,v)
        return v

