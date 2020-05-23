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
    Sets up empty board for each test

    Returns:
        (chess.Board)
    """
    game = chess.pgn.Game()
    board = game.board()
    return board


@pytest.fixture
def modified_boards() -> List[tuple]:
    """
    Sets up boards with modified FENs for testing. Includes
    move that should be taken

    Returns:
        {List[tuple]}
    """
    capture_black_knight = ('r1bqkbnr/ppp1pppp/8/3p4/3nP3/'
                            '2N2N2/PPP2PPP/R1B1KB1R w KQkq - 0 1')
    capture_black_queen = ('rnb1kbnr/pppp1ppp/8/3qp3/'
                           '4P3/5N2/PPP1QPPP/RNB1KB1R w KQkq - 0 1')
    capture_rook_or_knight = ('r1bqkbnr/pppppp1p/6p1/8/1n1B4/'
                              '2P5/PP2PPPP/RN1QKBNR w KQkq - 0 1')

    return [(chess.Board(fen=capture_black_knight), 'f3d4'),
            (chess.Board(fen=capture_black_queen), 'e4d5'),
            (chess.Board(fen=capture_rook_or_knight), 'd4h8')]


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
            AvoidCapture(),
            ScholarsMate()]


def test_base_engine(starting_board):
    """ Tests that errors are throwing properly if
    initialized without redefining evaluate & move"""
    eng = BaseEngine()
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


'''
def test_capture_highest_value_move(modified_boards):
    """ Tests that CaptureHighestValue captures highest value piece """
    engine = CaptureHighestValue()
    for board, rec_move in modified_boards:
        move = engine.move(board)
        assert str(move) == rec_move
'''
