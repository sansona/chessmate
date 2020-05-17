""" Basic tests for simulations. Note that since running
many simulations is computationally and time intensive, only
explicitly testing the simulation objects here and NOT
the engines themselves """
from simulations import *
from engines import *
from analysis import *
import chess
import chess.pgn
import pytest
import sys
sys.path.append('..')

N_GAMES = 10


@pytest.fixture
def setup_engines():
    """
    Sets up two computationally fastest engines
    for testing

    Returns:
            (List[ChessEngines])
    """
    return [AvoidCapture(), CaptureHighestValue()]


def test_single_game_results(setup_engines):
    """ Tests that game results stored properly """
    game = ChessPlayground(setup_engines[0], setup_engines[1])
    game.play_game()

    assert len(game.all_results) == 1
    assert isinstance(game.all_results[0], str)


def test_single_game_metadata(setup_engines):
    """ Tests that materials differences & game moves are being stored
    properly """
    game = ChessPlayground(setup_engines[0], setup_engines[1])
    game.play_game()

    assert isinstance(game.all_move_counts[0], int)
    assert len(game.all_material_differences[0]) == game.all_move_counts[0]


def test_multiple_games_results(setup_engines):
    """ Tests that results for multiple games stored properly """
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    simulator.play_multiple_games(N_GAMES)

    assert len(simulator.all_results) == N_GAMES
    assert all(isinstance(res, str) for res in simulator.all_results)


def test_multiple_games_metadata(setup_engines):
    """ Tests that metadata for multiple games stored properly """
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    simulator.play_multiple_games(N_GAMES)

    assert all(len(value_diff) == num_moves for value_diff, num_moves in zip(
        simulator.all_material_differences, simulator.all_move_counts))


def test_multiple_games_played(setup_engines):
    """ Tests that each game played is unique """
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    simulator.play_multiple_games(N_GAMES)

    assert len(set(simulator.all_move_counts)) != 1
    assert len(set(simulator.all_material_differences)) != 1
