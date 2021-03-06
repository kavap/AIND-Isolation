"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


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
    score = float(len(game.get_legal_moves(player)) - len(game.get_legal_moves(game.get_opponent(player))))

    return score


def custom_score_2(game, player):
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
    score = float(len(game.get_legal_moves(player)))
    return score


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
    score = float(len(game.get_legal_moves(player)) - 1.25*len(game.get_legal_moves(game.get_opponent(player))))
    return score


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
        """ In this case, we are simply letting the SearchTimeout return (-1,-1) [forfaiting the game]
        """


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

        level_to_evaluate = 1
        best_move_score = float("-inf")

        my_allowed_moves = game.get_legal_moves()

        if len(my_allowed_moves) == 0:
            return(-1,-1)

        if level_to_evaluate == depth:
            for move in my_allowed_moves:
                move_score = self.score(game.forecast_move(move),self)
                if move_score > best_move_score:
                    best_move_score = move_score
                    best_move = move
            return best_move
        else:
            (move_score,best_move) = self.max_value(game,depth,level_to_evaluate)
            return best_move


    def max_value(self,game, depth,level_to_evaluate):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move_score = float("-inf")
        best_move = (-1,-1)

        my_allowed_moves = game.get_legal_moves()

        if len(my_allowed_moves) == 0:
            return (best_move_score,(-1,-1))

        if level_to_evaluate == depth:
            for move in my_allowed_moves:
                move_score = self.score(game.forecast_move(move),self)
                if move_score > best_move_score:
                    best_move_score = move_score
                    best_move = move
            return (best_move_score,best_move)
        else:
            for move in my_allowed_moves:
                (opponent_score, opponent_move) = self.min_value(game.forecast_move(move),depth,level_to_evaluate+1)
                if opponent_score > best_move_score:
                    best_move_score = opponent_score
                    best_move = move
            return (best_move_score,best_move)


    def min_value(self,game, depth,level_to_evaluate):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        worst_move_score = float("inf")
        worst_move = (-1,-1)

        my_allowed_moves = game.get_legal_moves()

        if len(my_allowed_moves) == 0:
            return(worst_move_score,(-1,-1))

        if level_to_evaluate == depth:
            for move in my_allowed_moves:
                move_score = self.score(game.forecast_move(move),self)
                if move_score < worst_move_score:
                    worst_move_score = move_score
                    worst_move = move
            return (worst_move_score,worst_move)
        else:
            for move in my_allowed_moves:
                (opponent_score, opponent_move) = self.max_value(game.forecast_move(move),depth,level_to_evaluate+1)
                if opponent_score < worst_move_score:
                    worst_move_score = opponent_score
                    worst_move = move
            return (worst_move_score,worst_move)


class AlphaBetaPlayer(IsolationPlayer):

    def get_move(self, game, time_left):
        self.time_left = time_left
        best_move =  self.alphabeta(game,100) # Depth of 100 should be deep enough for the isolation agent
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        best_move = (-1, -1)

        my_allowed_moves = game.get_legal_moves()
        if len(my_allowed_moves) == 0:
            return best_move

        if depth == 0:  # I don't know if the tests are sending depth as 0 or 1 for level 1
            depth = 1

        try:
            for depth_limit in range(depth):
                if self.time_left() < self.TIMER_THRESHOLD:
                    break
                (move_score, best_move) = self.max_value(game, depth_limit+1, 1, alpha, beta)
        except SearchTimeout:
            return best_move
        return best_move

    def max_value(self,game, depth_limit,level_to_evaluate,alpha,beta):

       # print("in max")

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move_score = float("-inf")
        best_move = (-1,-1)

        my_allowed_moves = game.get_legal_moves()
        if len(my_allowed_moves) == 0:
            return (best_move_score,(-1,-1))

        if level_to_evaluate == depth_limit:
            for move in my_allowed_moves:
                if self.time_left() < self.TIMER_THRESHOLD:
                    raise SearchTimeout()
                move_score = self.score(game.forecast_move(move),self)
                if move_score > best_move_score:
                    best_move_score = move_score
                    best_move = move
            return (best_move_score,best_move)
        else:
            for i,move in enumerate(my_allowed_moves):
                (opponent_score, opponent_move) = self.min_value(game.forecast_move(move),depth_limit,level_to_evaluate+1,alpha,beta)
                if opponent_score > best_move_score:
                    best_move_score = opponent_score
                    best_move = move
                if best_move_score >= beta:
                    print("max valid moves:",my_allowed_moves)
                    print("max evaluated:",my_allowed_moves[:i+1])
                    print("max prunning:",my_allowed_moves[i+1:])
                    return (best_move_score,best_move)
                else:
                    alpha = max(best_move_score,alpha)
            return (best_move_score,best_move)


    def min_value(self,game, depth_limit,level_to_evaluate,alpha,beta):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        worst_move_score = float("inf")
        worst_move = (-1,-1)

        my_allowed_moves = game.get_legal_moves()
        if len(my_allowed_moves) == 0:
            return(worst_move_score,(-1,-1))

        if level_to_evaluate == depth_limit:
            for move in my_allowed_moves:
                if self.time_left() < self.TIMER_THRESHOLD:
                    raise SearchTimeout()
                move_score = self.score(game.forecast_move(move),self)
                if move_score < worst_move_score:
                    worst_move_score = move_score
                    worst_move = move
            return (worst_move_score,worst_move)
        else:
            for i,move in enumerate(my_allowed_moves):
                (opponent_score, opponent_move) = self.max_value(game.forecast_move(move),depth_limit,level_to_evaluate+1,alpha,beta)
                if opponent_score < worst_move_score:
                    worst_move_score = opponent_score
                    worst_move = move
                if worst_move_score <= alpha:
                    print("min valid moves:",my_allowed_moves)
                    print("min evaluated:",my_allowed_moves[:i+1])
                    print("min prunning:",my_allowed_moves[i+1:])
                    return (worst_move_score,worst_move)
                else:
                    beta = min(worst_move_score,beta)
            return (worst_move_score,worst_move)
