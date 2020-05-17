""" Test suite for engines """
from engines import *
from analysis import *
import chess
import chess.pgn
import pytest
import sys
sys.path.append('..')


@pytest.fixture
def starting_board():
    """
    Set ups empty board for each test

    Returns:
            (chess.Board)
    """
    game = chess.pgn.Game()
    board = game.board()
    return board


@pytest.fixture
def starting_engines():
    """
        Sets up fresh initializations of all engines
    Returns:
        (List)
    """
    return [Random(),
            PrioritizePawnMoves(),
            RandomCapture(),
            CaptureHighestValue(),
            AvoidCapture()]


def test_base_engine(starting_board):
    """ Tests that errors are throwing properly if
    initialized without redefining evaluate & move"""
    eng = ChessEngine()
    with pytest.raises(NotImplementedError):
        eng.evaluate(starting_board)
    with pytest.raises(NotImplementedError):
        eng.move(starting_board)


def test_evaluate_function(starting_engines, starting_board):
    """ Tests that each engine is able to evaluate
    a given board. As long as engines all evaluate board
    without error, pass test """
    for engine in starting_engines:
        engine.evaluate(starting_board)


def test_move_function(starting_engines, starting_board):
    """ Tests that each engine can return an appropriate
    move given starting_board. Assert that move is UCI Move """
    for engine in starting_engines:
        engine_move = engine.move(starting_board)
        assert isinstance(engine_move, chess.Move)
