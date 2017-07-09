"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    pass

def custom_score(game, player):
    score = float(len(game.get_legal_moves(player)) - len(game.get_legal_moves(game.get_opponent(player))))

    return score


def custom_score_2(game, player):
    score = float(len(game.get_legal_moves(player)))
    return score


def custom_score_3(game, player):
    score = float(len(game.get_legal_moves(player)) - 1.25*len(game.get_legal_moves(game.get_opponent(player))))
    return score


class IsolationPlayer:
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):

    def get_move(self, game, time_left):
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
        best_move = (-1,-1)
        self.time_left = time_left
        self.depth = 100
        try :
            for depth_limit in range(self.depth):
                best_move =  self.alphabeta(game,depth_limit+1) # Depth of 100 should be deep enough for the isolation agent
                if best_move == (-1,-1):
                    break
        except SearchTimeout:
            pass
        return best_move

    def alphabeta(self, game, depth_limit, alpha=float("-inf"), beta=float("inf")):

        best_move = (-1, -1)

        my_allowed_moves = game.get_legal_moves()
        if len(my_allowed_moves) == 0:
            return best_move

        if depth_limit == 0:  # I don't know if the tests are sending depth as 0 or 1 for level 1
            depth_limit = 1

        (move_score, best_move) = self.max_value(game, depth_limit, 1, alpha, beta)

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
                if best_move_score >= beta:
                    return (best_move_score,best_move)
                alpha = max(best_move_score,alpha)
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
                if worst_move_score <= alpha:
                    return (worst_move_score,worst_move)
                beta = min(worst_move_score,beta)
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
                beta = min(worst_move_score,beta)
            return (worst_move_score,worst_move)
