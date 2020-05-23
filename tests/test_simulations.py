""" Basic tests for simulations. Note that since running
many simulations is computationally and time intensive, only
explicitly testing the simulation objects here and NOT
the engines themselves """
import sys
from contextlib import contextmanager
import pytest
import chess
import chess.pgn
from simulations import *
from engines import AvoidCapture, CaptureHighestValue
from utils import not_raises

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


def test_playground_single_game_results(setup_engines):
    """ Tests that game results stored properly """
    game = ChessPlayground(setup_engines[0], setup_engines[1])
    game.play_game()

    assert len(game.all_results) == 1
    assert isinstance(game.all_results[0], str)


def test_playground_single_game_metadata(setup_engines):
    """ Tests that materials differences & game moves are being stored
    properly """
    game = ChessPlayground(setup_engines[0], setup_engines[1])
    game.play_game()

    assert isinstance(game.all_move_counts[0], int)
    assert len(game.all_material_differences[0]) == game.all_move_counts[0]


def test_playground_multiple_games_results(setup_engines):
    """ Tests that results for multiple games stored properly """
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    simulator.play_multiple_games(N_GAMES)

    assert len(simulator.all_results) == N_GAMES
    assert all(isinstance(res, str) for res in simulator.all_results)


def test_playground_multiple_games_metadata(setup_engines):
    """ Tests that metadata for multiple games stored properly """
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    simulator.play_multiple_games(N_GAMES)

    assert all(len(value_diff) == num_moves for value_diff, num_moves in zip(
        simulator.all_material_differences, simulator.all_move_counts))


def test_playground_multiple_games_played(setup_engines):
    """ Tests that each game played is unique """
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    simulator.play_multiple_games(N_GAMES)

    assert len(set(simulator.all_move_counts)) != 1
    assert len(set(simulator.all_material_differences)) != 1


def test_playvs_fen(setup_engines):
    """ Tests that setting up simulation w/ proper FEN works """
    playvs = PlayVsEngine(setup_engines[0])
    with not_raises(ValueError):
        playvs.fen = FEN_MAPS['standard']


def test_playvs_invalid_fen(setup_engines):
    """ Tests that setting up simulation w/ improper FEN raises error
    in PlayVsEngine"""
    playvs = PlayVsEngine(setup_engines[0])
    with pytest.raises(ValueError):
        playvs.fen = 'FAKE FEN STR'
    with pytest.raises(TypeError):
        playvs.fen = 0


def test_playground_valid_fen(setup_engines):
    """ Tests that setting up simulation w/ proper fen works"""
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    with not_raises(ValueError):
        simulator.fen = FEN_MAPS['standard']


def test_playground_invalid_fen(setup_engines):
    """ Tests that setting up simulation w/ improper FEN raises error
    in ChessPlayground"""
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    with pytest.raises(ValueError):
        simulator.fen = 'FAKE FEN STR'
    with pytest.raises(TypeError):
        simulator.fen = 0


def test_playvs_valid_player_side(setup_engines):
    """ Tests that setting up simulation w/ valid player side works """
    playvs = PlayVsEngine(setup_engines[1])
    with not_raises(ValueError):
        playvs.player_side = True
    with not_raises(ValueError):
        playvs.player_side = chess.WHITE


def test_playvs_invalid_player_side(setup_engines):
    """ Tests that setting up simulation w/ improper player side raises error
    in PlayVsEngine"""
    playvs = PlayVsEngine(setup_engines[1])
    with pytest.raises(TypeError):
        playvs.player_side = 'FAKE SIDE STR'
    with pytest.raises(TypeError):
        playvs.fen = 2


def test_playground_fen_retained(setup_engines):
    """ Tests that self.fen remains same value after playing games
    in ChessPlayground """
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    simulator.fen = FEN_MAPS['mayhem']
    simulator.play_multiple_games(N=N_GAMES)
    assert simulator.fen == FEN_MAPS['mayhem']


def test_all_fens_valid(setup_engines):
    """ Tests that able to play game with each FEN setup """
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    for f in FEN_MAPS:
        simulator.fen = FEN_MAPS[f]
        simulator.play_game()
        assert simulator.fen == FEN_MAPS[f]
