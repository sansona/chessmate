""" Test suite for engines """
import sys

import chess
import chess.pgn
import pytest

from constants import FEN_MAPS
from engines import *
from simulations import ChessPlayground

sys.path.append("..")


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
    capture_black_knight = (
        "r1bqkbnr/ppp1pppp/8/3p4/3nP3/" "2N2N2/PPP2PPP/R1B1KB1R w KQkq - 0 1"
    )
    capture_black_queen = (
        "rnb1kbnr/pppp1ppp/8/3qp3/" "4P3/5N2/PPP1QPPP/RNB1KB1R w KQkq - 0 1"
    )
    capture_rook_or_knight = (
        "r1bqkbnr/pppppp1p/6p1/8/1n1B4/" "2P5/PP2PPPP/RN1QKBNR w KQkq - 0 1"
    )

    return [
        (chess.Board(fen=capture_black_knight), "f3d4"),
        (chess.Board(fen=capture_black_queen), "e4d5"),
        (chess.Board(fen=capture_rook_or_knight), "d4h8"),
    ]


@pytest.fixture
def starting_engines():
    """
        Sets up fresh initializations of all engines
    Returns:
        (List)
    """
    return [
        Random(),
        PrioritizePawnMoves(),
        RandomCapture(),
        CaptureHighestValue(),
        AvoidCapture(),
        ScholarsMate(),
    ]


@pytest.fixture
def minimax_engines():
    """
    Sets up initializations of base minimax engines w/ depth 1
    Returns:
        (List)
    """

    return [
        MiniMax(color=chess.WHITE, depth=1),
        MiniMax(color=chess.BLACK, depth=1),
    ]


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


def test_random_capture_move(modified_boards):
    """ Tests that RandomCapture captures piece when available instead
    of moving randomly """
    engine = RandomCapture()
    black_knight_board = modified_boards[0][0]
    rec_move = modified_boards[0][1]
    move = engine.move(black_knight_board)
    assert str(move) == rec_move


def test_capture_highest_value_move(modified_boards):
    """ Tests that CaptureHighestValue captures highest value piece """
    engine = CaptureHighestValue()
    for board, rec_move in modified_boards:
        move = engine.move(board)
        assert str(move) == rec_move


def test_avoid_capture_move(modified_boards):
    """ Tests that AvoidCapture avoids captures """
    engine = AvoidCapture()
    for board, rec_move in modified_boards:
        move = engine.move(board)
        assert str(move) != rec_move


def test_scholars_mate_interrupt_resign():
    """ Tests that ScholarsMate resigns when any move is blocked """
    engine = ScholarsMate()

    # In both board states, white is interrupted from completed sequence
    blocked_queen_fen = (
        "r1bqkbnr/pppp1p1p/2n3p1/4p2Q/"
        "2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 1"
    )
    captured_queen_fen = (
        "r1b1kbnr/pppp1ppp/2n5/4p2q/" "2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 1"
    )

    for interrupted_fen in (blocked_queen_fen, captured_queen_fen):
        board = chess.Board(fen=interrupted_fen)
        assert engine.move(board) == chess.Move.null()


def test_scholars_mate_black_resign():
    """ Tests that ScholarsMate resigns if played on black """
    engine = ScholarsMate()

    board = chess.Board()
    board.push_uci("e2e4")
    assert engine.move(board) == chess.Move.null()


def test_scholars_mate_resign_failed_mate():
    """ Tests that ScholarsMate resigns if mate is not achieved
    after move sequence """
    engine = ScholarsMate()
    board = chess.Board()

    # After this sequence, white fails to mate black
    black_moves = ("e7e5", "d7d5", "b8c6", "e8f7")
    for move in black_moves:
        board.push_uci(str(engine.move(board)))
        board.push_uci(move)

    assert engine.move(board) == chess.Move.null()


@pytest.mark.slow
def test_minimax_depth_1_and_2_completion(minimax_engines):
    """ Tests that minimax at depths 1 & 2 doesn't hang """
    mm1 = minimax_engines[0]
    mm2 = minimax_engines[1]
    mm2.depth = 2
    simulation = ChessPlayground(mm1, mm2)
    simulation.fen = FEN_MAPS["easy_white_win"]
    simulation.play_game()


@pytest.mark.slow
def test_minimax_depth_3_completion(minimax_engines):
    """ Tests that minimax at depth 3 doesn't hang or return illegal moves.
    @ depth>=3, minimax evaluates own position in recursive call whereas @ depth<3,
    minimax only evaluates own position and opponents position once.
    This revisiting of own side's future position can lead to obscure bugs"""
    mm3 = minimax_engines[0]
    mm3.depth = 3
    simulation = ChessPlayground(mm3, ScholarsMate())
    simulation.fen = FEN_MAPS["easy_white_win"]
    simulation.play_game()


@pytest.mark.slow
def test_minimax_depth_4_completion(minimax_engines):
    """ Tests that minimax at depth 4 doesn't hang """
    engine = minimax_engines[1]
    engine.depth = 4
    simulation = ChessPlayground(CaptureHighestValue(), engine)
    simulation.fen = FEN_MAPS["easy_black_win"]
    simulation.play_game()


def test_minimax_depth_1_evaluation(minimax_engines, modified_boards):
    """ Tests that minimax depth 1 takes obvious captures """
    engine = minimax_engines[0]
    for board, rec_move in modified_boards:
        move = engine.move(board)
        assert str(move) == rec_move


def test_minimax_depth_2_evaluation(minimax_engines):
    """ Tests that minimax at depth 2 sees moves 2 steps ahead
    i.e obvious forks """
    black_knight_fork_fen = (
        "rnb1kb1r/ppppp1pp/8/8/3n4/8/" "PPPP1PPP/RNB1KBNR b KQkq - 0 1"
    )
    fork_boards = [(chess.Board(fen=black_knight_fork_fen), "d4c2")]

    engine = minimax_engines[1]
    engine.alpha_beta_pruning = False
    for board, rec_move in fork_boards:
        move = engine.move(board)
        assert str(move) == rec_move


def test_minimax_eval_side(minimax_engines):
    """ Tests that minimax evaluate function returns best move
    for own side i.e doesn't return best move for black when playing
    as white"""
    white_minimax, black_minimax = minimax_engines

    capture_black_queen = (
        f"rnb1kbnr/pppppppp/8/8/2q2Q2/8/" f"PPPPPPPP/RNB1KBNR w KQkq - 0 1"
    )
    capture_white_queen = (
        f"rnb1kbnr/pppppppp/8/8/2q2Q2/8/" f"PPPPPPPP/RNB1KBNR b KQkq - 0 1"
    )

    # White should capture blacks queen and vice-versa
    board = chess.Board(fen=capture_black_queen)
    assert str(white_minimax.move(board)) == "f4c4"

    board = chess.Board(fen=capture_white_queen)
    assert str(black_minimax.move(board)) == "c4f4"


@pytest.mark.slow
def test_minimax_no_pruning(minimax_engines):
    """ Test that without alpha beta pruning, minimax still evaluates
    obvious positions """
    white_minimax, black_minimax = minimax_engines
    white_minimax.alpha_beta_pruning = False
    black_minimax.alpha_beta_pruning = False

    capture_black_queen = (
        f"rnb1kbnr/pppppppp/8/8/2q2Q2/8/" f"PPPPPPPP/RNB1KBNR w KQkq - 0 1"
    )
    capture_white_queen = (
        f"rnb1kbnr/pppppppp/8/8/2q2Q2/8/" f"PPPPPPPP/RNB1KBNR b KQkq - 0 1"
    )

    # White should capture blacks queen and vice-versa
    board = chess.Board(fen=capture_black_queen)
    assert str(white_minimax.move(board)) == "f4c4"

    board = chess.Board(fen=capture_white_queen)
    assert str(black_minimax.move(board)) == "c4f4"
