""" Basic tests for simulations. Note that since running
many simulations is computationally and time intensive, only
explicitly testing the simulation objects here and NOT
the engines themselves """
from contextlib import contextmanager

import chess
import chess.pgn
import pytest

from chessmate.engines import AvoidCapture, CaptureHighestValue
from chessmate.simulations import *
from chessmate.utils import load_fen, not_raises

N_GAMES = 10


@pytest.fixture
def setup_engineplay():
    """ Sets up empty EnginePlay object """
    return EnginePlay()


@pytest.fixture
def setup_engines():
    """
    Sets up two computationally fastest engines
    for testing

    Returns:
        (List[ChessEngines])
    """
    return [AvoidCapture(), CaptureHighestValue()]


def test_engineplay_board_setter_with_valid_fen_no_errors(setup_engineplay):
    """ Tests that setting a valid FEN string to EnginePlay raises no
    errors """
    setup_engineplay.board = load_fen("in_progress_fen")


def test_engineplay_board_setter_with_invalid_fen_typeerror(setup_engineplay):
    """ Tests that setting an invalid FEN string to
    EnginePlay raises TypeError """
    with pytest.raises(TypeError):
        setup_engineplay.board = 0


def test_engineplay_fen_setter_with_invalid_fen_valueerror(setup_engineplay):
    """ Tests that setting an invalid FEN string to
    EnginePlay raises ValueError """
    with pytest.raises(ValueError):
        setup_engineplay.fen = "Invalid FEN string"


def test_engineplay_play_game_throws_notimplementederror(setup_engineplay):
    """ Tests that setting an invalid FEN string to
    EnginePlay raises valueerror """
    with pytest.raises(NotImplementedError):
        setup_engineplay.play_game()


def test_playvs_player_side_color_getter(setup_engines):
    """ Tests that player_side getter properly retrieves color """
    playvs = PlayVsEngine(setup_engines[0])
    with not_raises(ValueError):
        return playvs.player_side


def test_playvs_fen_setter(setup_engines):
    """ Tests that setting up simulation w/ proper FEN works """
    playvs = PlayVsEngine(setup_engines[0])
    with not_raises(ValueError):
        playvs.fen = FEN_MAPS["standard"]


def test_playvs_invalid_fen_setter(setup_engines):
    """ Tests that setting up simulation w/ improper FEN raises error
    in PlayVsEngine"""
    playvs = PlayVsEngine(setup_engines[0])
    with pytest.raises(ValueError):
        playvs.fen = "FAKE FEN STR"
    with pytest.raises(TypeError):
        playvs.fen = 0


def test_playvs_engine_move(setup_engines):
    """ Tests that playvs.engine_move function properly returns
    a legal move """
    playvs = PlayVsEngine(setup_engines[0])
    playvs.player_side = chess.BLACK
    assert isinstance(playvs.engine_move(), chess.Move)


def test_playground_valid_fen_setter(setup_engines):
    """ Tests that setting up simulation w/ proper fen works"""
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    with not_raises(ValueError):
        simulator.fen = FEN_MAPS["standard"]


def test_playground_invalid_fen_setter(setup_engines):
    """ Tests that setting up simulation w/ improper FEN raises error
    in ChessPlayground"""
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    with pytest.raises(ValueError):
        simulator.fen = "FAKE FEN STR"
    with pytest.raises(TypeError):
        simulator.fen = 0


def test_playvs_valid_player_side_setter(setup_engines):
    """ Tests that setting up simulation w/ valid player side works """
    playvs = PlayVsEngine(setup_engines[1])
    with not_raises(ValueError):
        playvs.player_side = True
    with not_raises(ValueError):
        playvs.player_side = chess.WHITE


def test_playvs_invalid_player_side_setter(setup_engines):
    """ Tests that setting up simulation w/ improper player side raises error
    in PlayVsEngine"""
    playvs = PlayVsEngine(setup_engines[1])
    with pytest.raises(TypeError):
        playvs.player_side = "FAKE SIDE STR"
    with pytest.raises(TypeError):
        playvs.fen = 2


def test_playground_single_game_stores_single_result(setup_engines):
    """ Tests that playground stores single result for single game """
    game = ChessPlayground(setup_engines[0], setup_engines[1])
    game.play_game()

    assert len(game.all_results) == 1
    assert isinstance(game.all_results[0], str)


def test_playground_single_game_stores_correct_len_metadata(setup_engines):
    """ Tests that materials differences & game moves are being stored
    properly """
    game = ChessPlayground(setup_engines[0], setup_engines[1])
    game.play_game()

    assert isinstance(game.all_move_counts[0], int)
    assert len(game.all_material_differences[0]) == game.all_move_counts[0]


def test_playground_multiple_games_stores_correct_len_results(setup_engines):
    """ Tests that correct number of results stored in play_multiple_games """
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    simulator.play_multiple_games(N_GAMES)

    assert len(simulator.all_results) == N_GAMES
    assert all(isinstance(res, str) for res in simulator.all_results)


def test_playground_multiple_games_stores_corect_len_metadata(setup_engines):
    """ Tests that correct length of metadata stored for play_multiple_games """
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    simulator.play_multiple_games(N_GAMES)

    assert all(
        len(value_diff) == num_moves
        for value_diff, num_moves in zip(
            simulator.all_material_differences, simulator.all_move_counts
        )
    )


def test_playground_multiple_games_plays_unique_games(setup_engines):
    """ Tests that each game played via play_multiple_games is unique """
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    simulator.play_multiple_games(N_GAMES)

    assert len(set(simulator.all_move_counts)) != 1
    assert len(set(simulator.all_material_differences)) != 1


def test_playground_fen_retained(setup_engines):
    """ Tests that self.fen remains same value after playing games
    in ChessPlayground """
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    simulator.fen = FEN_MAPS["mayhem"]
    simulator.play_multiple_games(N=N_GAMES)
    assert simulator.fen == FEN_MAPS["mayhem"]


def test_all_fen_maps_are_valid_positions(setup_engines):
    """ Tests that each fen value in constants.FEN_MAPS is a valid position"""
    simulator = ChessPlayground(setup_engines[0], setup_engines[1])
    for f in FEN_MAPS:
        simulator.fen = FEN_MAPS[f]
        simulator.play_game()
        assert simulator.fen == FEN_MAPS[f]
