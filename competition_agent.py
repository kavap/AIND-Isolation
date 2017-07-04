"""Implement your own custom search agent using any combination of techniques
you choose.  This agent will compete against other students (and past
champions) in a tournament.

         COMPLETING AND SUBMITTING A COMPETITION AGENT IS OPTIONAL
"""


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

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
    score = len(game.get_legal_moves(player)) - 1.25*len(game.get_legal_moves(game.get_opponent(player)))
    return score


class CustomPlayer:
    """Game-playing agent to use in the optional player vs player Isolation
    competition.

    You must at least implement the get_move() method and a search function
    to complete this class, but you may use any of the techniques discussed
    in lecture or elsewhere on the web -- opening books, MCTS, etc.

    **************************************************************************
          THIS CLASS IS OPTIONAL -- IT IS ONLY USED IN THE ISOLATION PvP
        COMPETITION.  IT IS NOT REQUIRED FOR THE ISOLATION PROJECT REVIEW.
    **************************************************************************

    Parameters
    ----------
    data : string
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted.  Note that
        the PvP competition uses more accurate timers that are not cross-
        platform compatible, so a limit of 1ms (vs 10ms for the other classes)
        is generally sufficient.
    """

    def __init__(self, data=None, timeout=10.):
        self.score = custom_score
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
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
        best_move = self.iterativeDeepening(game, time_left, self.TIMER_THRESHOLD)

        return best_move

    def iterativeDeepening(self, game, time_left, timer_threshold):

        best_move = (-1, -1)
        try:
            for depth in range(1000):  # Depth of 1000 should be deep enough for the isolation agent
                if time_left() < timer_threshold:
                    return best_move
                level_move = self.alphabeta(game, depth + 1, time_left, timer_threshold)
                best_move = level_move
                if level_move == (-1, -1):
                    return (-1, -1)
        except SearchTimeout:
            return best_move

    def alphabeta(self, game, depth, time_left, timer_threshold, alpha=float("-inf"), beta=float("inf")):
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
        if time_left() < timer_threshold:
            raise SearchTimeout()

        level_to_evaluate = 1
        best_move_score = float("-inf")

        my_allowed_moves = game.get_legal_moves()

        if len(my_allowed_moves) == 0:
            return (-1, -1)

        if level_to_evaluate == depth:
            for move in my_allowed_moves:
                move_score = self.score(game.forecast_move(move), self)
                if move_score > best_move_score:
                    best_move_score = move_score
                    best_move = move
                return best_move
        else:
            (move_score, best_move) = self.max_value(game, depth, level_to_evaluate, time_left, timer_threshold, alpha,
                                                     beta)
            return best_move

    def max_value(self, game, depth, level_to_evaluate, time_left, timer_threshold, alpha, beta):

        if time_left() < timer_threshold:
            raise SearchTimeout()

        best_move_score = float("-inf")
        best_move = (-1, -1)

        my_allowed_moves = game.get_legal_moves()

        if len(my_allowed_moves) == 0:
            return (best_move_score, (-1, -1))

        if level_to_evaluate == depth:
            for move in my_allowed_moves:
                move_score = self.score(game.forecast_move(move), self)
                if move_score > best_move_score:
                    best_move_score = move_score
                    best_move = move
                return (best_move_score, best_move)
        else:
            for move in my_allowed_moves:
                (opponent_score, opponent_move) = self.min_value(game.forecast_move(move), depth, level_to_evaluate + 1,
                                                                 time_left, timer_threshold, alpha, beta)
                if opponent_score > best_move_score:
                    best_move_score = opponent_score
                    best_move = move
                if best_move_score >= beta:
                    return (best_move_score, best_move)
                else:
                    alpha = max(best_move_score, alpha)
            return (best_move_score, best_move)

    def min_value(self, game, depth, level_to_evaluate, time_left, timer_threshold, alpha, beta):

        if time_left() < timer_threshold:
            raise SearchTimeout()

        worst_move_score = float("inf")
        worst_move = (-1, -1)

        my_allowed_moves = game.get_legal_moves()

        if len(my_allowed_moves) == 0:
            return (worst_move_score, (-1, -1))

        if level_to_evaluate == depth:
            for move in my_allowed_moves:
                move_score = self.score(game.forecast_move(move), self)
                if move_score < worst_move_score:
                    worst_move_score = move_score
                    worst_move = move
                return (worst_move_score, worst_move)
        else:
            for move in my_allowed_moves:
                (opponent_score, opponent_move) = self.max_value(game.forecast_move(move), depth, level_to_evaluate + 1,
                                                                 time_left, timer_threshold, alpha, beta)
                if opponent_score < worst_move_score:
                    worst_move_score = opponent_score
                    worst_move = move
                if worst_move_score <= alpha:
                    return (worst_move_score, worst_move)
                else:
                    beta = min(worst_move_score, beta)
            return (worst_move_score, worst_move)
