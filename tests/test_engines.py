""" Test suite for engines """
import sys
from typing import List

import chess  # type: ignore
import chess.pgn  # type: ignore
from chessmate.constants.fens import FEN_MAPS
from chessmate.engines import *
from chessmate.simulations import ChessPlayground
from chessmate.utils import load_fen

import pytest  # type: ignore

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
    return [
        (chess.Board(fen=load_fen("capture_black_knight")), "f3d4"),
        (chess.Board(fen=load_fen("capture_black_queen")), "e4d5"),
        (chess.Board(fen=load_fen("capture_rook_or_knight")), "d4h8"),
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


def test_base_engine_move_function_no_errors(starting_board):
    """ Tests that errors are throwing properly if
    initialized without redefining evaluate & move"""
    eng = BaseEngine()
    with pytest.raises(NotImplementedError):
        eng.evaluate(starting_board)
    with pytest.raises(NotImplementedError):
        eng.move(starting_board)


def test_evaluate_function_no_errors(starting_engines, starting_board):
    """ Tests that each engine is able to evaluate
    a given board. As long as engines all evaluate board
    without error, pass test """
    for engine in starting_engines:
        engine.evaluate(starting_board)


def test_move_function_returns_move(starting_engines, starting_board):
    """ Tests that each engine can return an appropriate
    move given starting_board. Assert that move is UCI Move """
    for engine in starting_engines:
        engine_move = engine.move(starting_board)
        assert isinstance(engine_move, chess.Move)


def test_random_capture_move_captures_when_available(modified_boards):
    """ Tests that RandomCapture captures piece when available instead
    of moving randomly """
    engine = RandomCapture()
    black_knight_board = modified_boards[0][0]
    rec_move = modified_boards[0][1]
    move = engine.move(black_knight_board)
    assert str(move) == rec_move


def test_capture_highest_value_move_captures_highest_value(modified_boards):
    """ Tests that CaptureHighestValue captures highest value piece """
    engine = CaptureHighestValue()
    for board, rec_move in modified_boards:
        move = engine.move(board)
        assert str(move) == rec_move


def test_prioritize_pieces_chooses_correct_move(versatile_board):
    """ Tests the same board for different pieces """
    board = chess.Board(fen=load_fen("anyone_captures_queen"))
    versatile_board = [
        ("h4g5", "p"),
        ("c1g5", "B"),
        ("f3g5", "n"),
        ("g3g5", "R"),
        ("e5g5", "q"),
    ]
    for i in range(0, len(versatile_board)):
        engine = PrioritizePieceMoves(versatile_board[i][1])
        rec_move = versatile_board[i][0]
        move = engine.move(board)
        assert str(move) == rec_move


def test_avoid_capture_move_avoids_available_captures(modified_boards):
    """ Tests that AvoidCapture avoids captures """
    engine = AvoidCapture()
    for board, rec_move in modified_boards:
        move = engine.move(board)
        assert str(move) != rec_move


def test_scholars_mate_resigns_when_sequence_interrupted():
    """ Tests that ScholarsMate resigns when any move is blocked """
    engine = ScholarsMate()

    # In both board states, white is interrupted from completed sequence
    interrupted_fen_sequences = [
        load_fen("blocked_queen_fen"),
        load_fen("captured_queen_fen"),
    ]

    for interrupted_fen in interrupted_fen_sequences:
        board = chess.Board(fen=interrupted_fen)
        assert engine.move(board) == chess.Move.null()


def test_scholars_mate_resign_if_played_on_black():
    """ Tests that ScholarsMate resigns if played on black """
    engine = ScholarsMate()

    board = chess.Board()
    board.push_uci("e2e4")
    assert engine.move(board) == chess.Move.null()


def test_scholars_mate_resign_after_failed_mate():
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


def test_minimax_set_depth_to_str_raises_typeerror():
    """ Tests that minimax depth setter function will raise TypeError
    if string is passed to depth """
    mm = MiniMax(color=chess.WHITE, depth=1)
    with pytest.raises(TypeError):
        mm.depth = "one"


def test_minimax_set_depth_to_str_raises_typeerror():
    """ Tests that minimax depth setter function will raise ValueError
    if int < 1 is passed to depth """
    mm = MiniMax(color=chess.WHITE, depth=1)
    with pytest.raises(ValueError):
        mm.depth = 0
    with pytest.raises(ValueError):
        mm.depth = -1


def test_minimax_evaluate_invalid_color_raises_valueerror():
    """ Tests that calling minimax evaluate function with
    non-bool color raises ValueError"""
    mm = MiniMax(color=chess.WHITE, depth=1)
    mm.color = "white"
    with pytest.raises(ValueError):
        mm.evaluate(chess.Board())


@pytest.mark.slow
def test_minimax_depth_1_and_2_game_completion(minimax_engines):
    """ Tests that minimax at depths 1 & 2 doesn't hang """
    mm1 = minimax_engines[0]
    mm2 = minimax_engines[1]
    mm2.depth = 2
    simulation = ChessPlayground(mm1, mm2)
    simulation.fen = FEN_MAPS["easy_white_win"]
    simulation.play_game()


@pytest.mark.slow
def test_minimax_depth_3_game_completion(minimax_engines):
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
def test_minimax_depth_4_game_completion(minimax_engines):
    """ Tests that minimax at depth 4 doesn't hang """
    engine = minimax_engines[1]
    engine.depth = 4
    simulation = ChessPlayground(CaptureHighestValue(), engine)
    simulation.fen = FEN_MAPS["easy_black_win"]
    simulation.play_game()


def test_minimax_depth_1_evaluation_captures(minimax_engines, modified_boards):
    """ Tests that minimax depth 1 takes obvious captures """
    engine = minimax_engines[0]
    for board, rec_move in modified_boards:
        move = engine.move(board)
        assert str(move) == rec_move


def test_minimax_depth_2_evaluation_captures(minimax_engines):
    """ Tests that minimax at depth 2 sees moves 2 steps ahead
    i.e obvious forks """

    fork_boards = [
        (chess.Board(fen=load_fen("black_knight_fork_fen")), "d4c2")
    ]

    engine = minimax_engines[1]
    engine.alpha_beta_pruning = False
    for board, rec_move in fork_boards:
        move = engine.move(board)
        assert str(move) == rec_move


def test_minimax_evaluates_correct_side(minimax_engines):
    """ Tests that minimax evaluate function returns best move
    for own side i.e doesn't return best move for black when playing
    as white"""
    white_minimax, black_minimax = minimax_engines

    # White should capture blacks queen and vice-versa
    board = chess.Board(fen=load_fen("capture_black_queen_2"))
    assert str(white_minimax.move(board)) == "f4c4"

    board = chess.Board(fen=load_fen("capture_white_queen_2"))
    assert str(black_minimax.move(board)) == "c4f4"


@pytest.mark.slow
def test_minimax_no_pruning_captures_obvious_pieces(minimax_engines):
    """ Test that without alpha beta pruning, minimax still evaluates
    obvious positions """
    white_minimax, black_minimax = minimax_engines
    white_minimax.alpha_beta_pruning = False
    black_minimax.alpha_beta_pruning = False

    # White should capture blacks queen and vice-versa
    board = chess.Board(fen=load_fen("capture_black_queen_2"))
    assert str(white_minimax.move(board)) == "f4c4"

    board = chess.Board(fen=load_fen("capture_white_queen_2"))
    assert str(black_minimax.move(board)) == "c4f4"
