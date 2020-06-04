""" Test suite for assortment of analysis functions """
import chess  # type: ignore
import chess.pgn  # type: ignore
import pytest  # type: ignore

from analysis import *


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
def in_progress_board():
    """
    Set ups board of an in progress game

    Returns:
        (chess.Board)
    """
    in_progress_fen = (
        "2kr1bnr/2ppqppp/p7/2p1p3/" "3PP3/2N2N2/PPP2PPP/R1BQK2R w KQk - 0 1"
    )
    board = chess.Board(fen=in_progress_fen)
    return board


@pytest.fixture
def not_mated_boards():
    """
    Sets up boards that ended due to resignation

    Returns:
        List[chess.Board]
    """
    not_mated_fen = [
        (
            "r1b1kbnr/ppp1qQp1/2np3p/4p3/"
            "2BNP3/8/PPPP1PPP/RNB1K2R w KQkq - 0 1"
        ),
        ("rnbqkbnr/pp1ppppp/2p5/8/" "4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 1 2"),
    ]

    return [chess.Board(fen=f) for f in not_mated_fen]


@pytest.fixture
def stalemate_boards():
    """
    Sets up boards that ended due to stalemate

    Returns:
        List[chess.Board]
    """
    stalemate_fen = [
        "8/8/8/8/8/4k3/4p3/4K3 w - - 0 1",
        "8/8/8/8/8/4k3/4p3/4K3 w - - 0 1",
    ]

    return [chess.Board(fen=f) for f in stalemate_fen]


@pytest.fixture
def evaluation_engines():
    """
    Sets up evaluation engines

    Returns:
        (List)
    """
    return [StandardEvaluation(), PiecePositionEvaluation()]


def test_evaluate_ending_for_white_win_position():
    """ Tests that boards correspond to mate are correctly evaluated """
    white_to_mate = chess.Board(fen="8/8/8/2Q1k3/6Q1/3Q1Q2/4K3/8 w - - 0 1")
    white_to_mate.push_uci("d3e4")

    assert evaluate_ending_board(white_to_mate) == "White win by mate"


def test_evaluate_ending_for_not_mated_positions(not_mated_boards):
    """ Tests that boards ending in resignation are correctly evaluated """
    for board in not_mated_boards:
        assert evaluate_ending_board(board) == "Game over by resignation"


def test_evaluate_ending_for_stalemate_positions(stalemate_boards):
    """ Tests that boards ending in stalemate are correctly evaluated """
    for board in stalemate_boards:
        assert evaluate_ending_board(board) == "Stalemate"


def test_standard_eval_starting_board_values(starting_board):
    """ Tests that StandardEvaluation.evaluate is
    properly evaluating initial board state """
    starting_board_value = StandardEvaluation().evaluate(starting_board)
    assert starting_board_value == 0


def test_base_eval_function_raises_notimplementederror_for_evaluate():
    """ Tests that evaluate function raises NotImplementedError if
    evaluate called """
    evalfunc = EvaluationFunction()
    with pytest.raises(NotImplementedError):
        evalfunc.evaluate(chess.Board)


def test_standard_eval_after_replacement_values(starting_board):
    """ Tests that StandardEvaluation.evaluate evaluates same value
    after removing and replacing piece i.e no effect on evaluation from
    removing and resetting a piece """
    starting_board.set_piece_at(chess.E1, chess.Piece(6, chess.WHITE))
    value_after_replacement = StandardEvaluation().evaluate(starting_board)
    assert value_after_replacement == 0


def test_standard_eval_after_exchange_values(starting_board):
    """ Tests that StandardEvaluation.evaluate evaluates correct
    value on board after exchange of pieces """
    # Remove one black bishop and white queen
    starting_board.remove_piece_at(chess.C8)
    starting_board.remove_piece_at(chess.D1)
    value_after_exchange = StandardEvaluation().evaluate(starting_board)
    black_bishop_white_queen_value_difference = -650
    assert value_after_exchange == black_bishop_white_queen_value_difference


def test_standard_eval_in_progress_board_values(in_progress_board):
    """ Tests that StandardEvaluation.evaluate is
    properly evaluating in progress board state """
    in_progress_board_value = StandardEvaluation().evaluate(in_progress_board)
    in_progress_known_difference = 350
    assert in_progress_board_value == in_progress_known_difference


def test_standard_eval_after_capture_values(starting_board):
    """ Tests that StandardEvaluation.evaluate is properly
    evaluating board state after capture """
    starting_board.remove_piece_at(chess.E1)
    value_no_white_king = StandardEvaluation().evaluate(starting_board)
    missing_white_king_value = -99999
    assert value_no_white_king == missing_white_king_value


def test_piece_position_eval_starting_board_values(starting_board):
    """ Tests that piece_value_eval properly calculates values
    for starting board"""
    piece_val = PiecePositionEvaluation()
    starting_board_known_value = -340
    assert piece_val.evaluate(starting_board) == starting_board_known_value


def test_piece_position_eval_in_progress_board_values(in_progress_board):
    """ Tests that piece_value_eval properly calculates values
    for a board in progress """
    piece_val = PiecePositionEvaluation()
    in_progress_position_value = 231
    assert piece_val.evaluate(in_progress_board) == in_progress_position_value
