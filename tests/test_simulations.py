""" Basic tests for simulations. Note that since running
many simulations is computationally and time intensive, only
explicitly testing the simulation objects here and NOT
the engines themselves """
from simulations import *
from engines import *
import chess
import chess.pgn
import pytest
import sys
sys.path.append('..')


@pytest.fixture
def setup_engines():
    """
    Sets up two computationally fastest engines
    for testing

    Returns:
            (List[ChessEngines])
    """
    return [Random(), CaptureHighestValue()]


def test_single_game(setup_engines):
    """ Tests that game metadata stored properly """
    game = ChessPlayground(setup_engines[0], setup_engines[1])
    game.play_game()

    assert len(game.all_results) == 1
    assert isinstance(game.all_results[0], str)
    assert isinstance(game.all_move_counts[0], int)
    assert len(game.all_value_differentials[0]) == game.all_move_counts[0]


def test_multiple_games(setup_engines, n_games=10):
    """ Tests that multiple games can be played and data is stored properly """
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    simulator.play_multiple_games(n_games)

    assert len(simulator.all_results) == n_games
    assert all(isinstance(res, str) for res in simulator.all_results)
    assert all(isinstance(
        move_count, int) for move_count in simulator.all_move_counts)
    assert all(len(value_diff) == num_moves for value_diff, num_moves in zip(
        simulator.all_value_differentials, simulator.all_move_counts))
