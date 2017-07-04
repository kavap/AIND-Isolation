"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest
import timeit

import isolation
import game_agent
import sample_players

from importlib import reload

from isolation.isolation import TIME_LIMIT_MILLIS

"""
TestBoard is clone of isolation.Board except for "play" method. The play method of TestBoard
allows the test methods to play one move at a time. Also note that when a player looses and 
returns (-1,-1), new "play" method provides better winner information to caller. To play the 
game to end, call "play" method with number_of_moves = float("inf")
"""
class TestBoard(isolation.Board):

    move_history = []
    CONCESSION_MOVE = (-1,-1)



    def play(self,time_limit=TIME_LIMIT_MILLIS,number_of_moves=float("inf")):

        time_millis = lambda: 1000 * timeit.default_timer()

        moves_so_far = 0

        while True:

            legal_player_moves = self.get_legal_moves()
            game_copy = self.copy()

            move_start = time_millis()
            time_left = lambda: time_limit - (time_millis() - move_start)
            print(game_copy.print_board())
            print(self._board_state)
            curr_move = self._active_player.get_move(game_copy, time_left)
            print(curr_move)
            move_end = time_left()

            if curr_move is None:
                curr_move = TestBoard.NOT_MOVED

            if move_end < 0:
                return self._inactive_player, self.move_history, "timeout"

            if curr_move == self.CONCESSION_MOVE:
                if self._inactive_player == self._player_1:
                    return self._inactive_player, self.move_history, "player_1 wins"
                else:
                    return self._inactive_player, self.move_history, "player_2 wins"

            if curr_move not in legal_player_moves:
                if len(legal_player_moves) > 0:
                    return self._inactive_player, self.move_history, "forfeit"
                return self._inactive_player, self.move_history, "illegal move"

            self.move_history.append(list(curr_move))

            self.apply_move(curr_move)

            moves_so_far += 1

            if moves_so_far >= number_of_moves:
                break

        return self._active_player,self.move_history,"game-on"






class TestAlphaBetaPlayer(unittest.TestCase):

    my_player = None
    opponent = None
    game_board_1 = None # Board with my_player as player_1
    game_board_2 = None # Board with my_player as player_2
    game_board_3 = None # Board with my_player set to search 5 levels deep
    game_board_4 = None # Board with my_player set to search 10 levels deep
    game_board_5 = None # Board with my_player set to search 3 levels deep and
                             # scoreing function = custom_score_2
    game_board_6 = None # Board with my_player set to search 3 levels deep and
                             # scoreing function = custom_score_3


    def reset_boards(self):
        self.my_player = game_agent.AlphaBetaPlayer(2,sample_players.open_move_score,10)
        self.opponent = sample_players.GreedyPlayer(sample_players.open_move_score)
        self.game_board_1 = TestBoard(self.my_player, self.opponent,9,9)
        self.game_board_2 = TestBoard(self.opponent,self.my_player,9,9)
        self.my_player = game_agent.AlphaBetaPlayer(5,game_agent.custom_score,10)
        self.game_board_3 = TestBoard(self.my_player, self.opponent,9,9)
        self.my_player = game_agent.AlphaBetaPlayer(10,game_agent.custom_score,10)
        self.game_board_4 = TestBoard(self.my_player, self.opponent,9,9)
        self.my_player = game_agent.AlphaBetaPlayer(3,game_agent.custom_score_2,10)
        self.game_board_5 = TestBoard(self.my_player, self.opponent,9,9)
        self.my_player = game_agent.AlphaBetaPlayer(3,game_agent.custom_score_3,10)
        self.game_board_6 = TestBoard(self.my_player, self.opponent,9,9)


    def setUp(self):
        reload(game_agent)
        self.reset_boards()
    def test_why_given_board_is_forfeit(self):
        self.reset_boards()
        self.game_board_1._board_state = [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,0,1,1,0,1,1,0,0,0,0,1,0,0,0,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,0,0,1,0,46,71,24]
        self.assertIn(self.game_board_1.play(2000)[2],["player_1 wins","player_2 wins"],"Your agent timed out or made illegal move")

"""
    def test_can_make_one_valid_move(self):
        self.assertEqual(self.game_board_1.play(2000,1)[2],"game-on","Your agent cant make even a single valid move")

    def test_prunning_for_given_board(self):
        self.reset_boards()
        self.game_board_1._board_state = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,46,47,46]
        self.assertIn(self.game_board_1.play(2000)[2],["player_1 wins","player_2 wins"],"Your agent timed out or made illegal move")
"""

"""
    def test_makes_all_legal_moves_throughout_the_game(self):
        self.assertNotEqual(self.game_board_1.play(2000,float("inf"))[2],"illegal move","Your agent made an illegal move")

    def test_gracefully_indicates_victory_or_loss(self):
        self.reset_boards()
        self.assertIn(self.game_board_1.play(2000,float("inf"))[2],["player_1 wins","player_2 wins"],"Your agent timed out or made illegal move")

    def test_can_complete_move_in_5_sec(self):
        self.reset_boards()
        self.assertNotEqual(self.game_board_1.play(5000,float("inf"))[2],"timeout","Your agent timed out")

    def test_can_complete_move_in_2_sec(self):
        self.reset_boards()
        self.assertNotEqual(self.game_board_1.play(2000,float("inf"))[2],"timeout","Your agent timed out")

    def test_can_search_to_depth_5_in_2_sec(self):
        self.reset_boards()
        self.assertNotEqual(self.game_board_3.play(2000,float("inf"))[2],"timeout","Your agent timed out")

    def test_can_search_to_depth_10_in_2_sec(self):
        self.reset_boards()
        self.assertNotEqual(self.game_board_4.play(2000,float("inf"))[2],"timeout","Your agent timed out")

    def test_wins_using_scoring_function(self):
        self.reset_boards()
        self.assertEqual(self.game_board_1.play(2000,float("inf"))[2],"player_1 wins","Your agent didn't win with scoring function")

    def test_wins_using_scoring_function_2(self):
        self.reset_boards()
        self.assertEqual(self.game_board_5.play(2000,float("inf"))[2],"player_1 wins","Your agent didn't win with scoring function 2")

    def test_wins_using_scoring_function_3(self):
        self.reset_boards()
        self.assertEqual(self.game_board_6.play(2000,float("inf"))[2],"player_1 wins","Your agent didn't win with scoring function 3")
"""

if __name__ == '__main__':
    unittest.main()
