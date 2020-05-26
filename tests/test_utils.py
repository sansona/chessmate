""" Test suite for assortment of helper functions """
import sys
import pytest
import chess
import chess.pgn
from utils import *
from analysis import tabulate_board_values

sys.path.append("..")


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
    Set ups in progress board

    Returns:
        (chess.Board)
    """
    in_progress_fen = (
        "2kr1bnr/2ppqppp/p7/2p1p3/" "3PP3/2N2N2/PPP2PPP/R1BQK2R w KQk - 0 1"
    )
    board = chess.Board(fen=in_progress_fen)
    return board


def test_starting_board_piece_at_function(starting_board):
    """ Tests that piece at function returns
    value of piece at square in starting position"""
    rook = get_piece_at(starting_board, chess.A8)
    king = get_piece_at(starting_board, "e1")
    pawn = get_piece_at(starting_board, "e2")
    empty_piece = get_piece_at(starting_board, "C3")

    assert rook == "r"
    assert king == "K"
    assert pawn == "P"
    assert not empty_piece


def test_inprogress_board_piece_at_function(in_progress_board):
    """ Tests that piece at function returns
    value of piece at square in agame in progress"""
    pawn = get_piece_at(in_progress_board, "e4")
    queen = get_piece_at(in_progress_board, chess.E7)
    empty_piece = get_piece_at(in_progress_board, "F1")

    assert pawn == "P"
    assert queen == "q"
    assert not empty_piece


def test_tabulate_starting_board_values(starting_board):
    """ Tests that tabulate board values function is
    properly evaluating initial board state """
    starting_board_value = tabulate_board_values(starting_board)
    assert starting_board_value == 0

    # Replace white king
    starting_board.set_piece_at(chess.E1, chess.Piece(6, chess.WHITE))
    replace_white_king_value = tabulate_board_values(starting_board)
    assert replace_white_king_value == 0

    # Remove one black bishop and white queen
    starting_board.remove_piece_at(chess.C8)
    starting_board.remove_piece_at(chess.D1)
    trade_wqueen_bbishop_value = tabulate_board_values(starting_board)
    assert trade_wqueen_bbishop_value == -6.0


def test_tabulate_in_progress_board_values(in_progress_board):
    """ Tests that tabulate board values function is
    properly evaluating in progress board state """
    in_progress_board_value = tabulate_board_values(in_progress_board)
    assert in_progress_board_value == 3.0


def test_tabulate_after_capture_values(starting_board):
    """ Tests that tabulate board values function is properly
    evaluating board state after capture """
    starting_board_value = tabulate_board_values(starting_board)
    starting_board.remove_piece_at(chess.E1)
    no_white_king_value = tabulate_board_values(starting_board)
    assert no_white_king_value == -999.0


def test_tabulate_after_replacement_values(starting_board):
    """ Tests that tabulate board values function is properly
    evaluating board state after capture and replacement"""
    starting_board_value = tabulate_board_values(starting_board)

    # Remove and replace white king with itself
    starting_board.remove_piece_at(chess.E1)
    starting_board.set_piece_at(chess.E1, chess.Piece(6, chess.WHITE))
    replacement_value = tabulate_board_values(starting_board)

    assert replacement_value == 0


def test_tabulate_after_trade_values(starting_board):
    """ Tests that tabulate board values function is properly
    evaluating board state after trading pieces of uneven value"""
    starting_board_value = tabulate_board_values(starting_board)

    # Remove one black bishop and white queen
    starting_board.remove_piece_at(chess.C8)
    starting_board.remove_piece_at(chess.D1)
    trade_wqueen_bbishop_value = tabulate_board_values(starting_board)
    assert trade_wqueen_bbishop_value == -6.0
