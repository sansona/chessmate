""" Test suite for assortment of helper functions """
import sys

import chess
import chess.pgn
import pytest

from analysis import tabulate_board_values
from utils import *

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
    Set ups board of an in progress game

    Returns:
        (chess.Board)
    """
    in_progress_fen = (
        "2kr1bnr/2ppqppp/p7/2p1p3/" "3PP3/2N2N2/PPP2PPP/R1BQK2R w KQk - 0 1"
    )
    board = chess.Board(fen=in_progress_fen)
    return board


def test_piece_at_function_on_starting_position(starting_board):
    """ Tests that piece_at function returns correct
    symbol of piece at square in starting position"""
    piece_at_rook_square = get_piece_at(starting_board, chess.A8)
    piece_at_king_square = get_piece_at(starting_board, "e1")
    piece_at_pawn_square = get_piece_at(starting_board, "e2")

    assert piece_at_rook_square == "r"
    assert piece_at_king_square == "K"
    assert piece_at_pawn_square == "P"


def test_piece_at_function_on_empty_square(starting_board):
    """ Tests that piece_at function returns False for
    empty squares """
    piece_at_empty_square = get_piece_at(starting_board, "C3")
    assert not piece_at_empty_square


def test_piece_at_function_on_inprogress_board(in_progress_board):
    """ Tests that piece at function returns
    value of piece at square in a game in progress"""
    piece_at_square_occupied_by_pawn = get_piece_at(in_progress_board, "e4")
    piece_at_square_occupied_by_queen = get_piece_at(
        in_progress_board, chess.E7)

    assert piece_at_square_occupied_by_pawn == "P"
    assert piece_at_square_occupied_by_queen == "q"


def test_piece_at_function_on_empty_square_inprogress_board(in_progress_board):
    """ Tests that piece at function returns False for empty square
    for a board that's not the starting board """
    piece_at_empty_square = get_piece_at(in_progress_board, "F1")
    assert not piece_at_empty_square


def test_tabulate_starting_board_values(starting_board):
    """ Tests that tabulate board values function is
    properly evaluating initial board state """
    starting_board_value = tabulate_board_values(starting_board)
    assert starting_board_value == 0


def test_tabulate_starting_board_values_after_replacement(starting_board):
    """ Tests that tabulate board values function evaluates same value
    after removing and replacing piece i.e no effect on evaluation from
    removing and resetting a piece """
    starting_board.set_piece_at(chess.E1, chess.Piece(6, chess.WHITE))
    value_after_replacement = tabulate_board_values(starting_board)
    assert value_after_replacement == 0


def test_tabulate_starting_board_values_after_exchange(starting_board):
    """ Tests that tabulate board values function evaluates correct
    value on board after exchange of pieces """
    # Remove one black bishop and white queen
    starting_board.remove_piece_at(chess.C8)
    starting_board.remove_piece_at(chess.D1)
    value_after_exchange = tabulate_board_values(starting_board)
    assert value_after_exchange == -6.0


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
    value_no_white_king = tabulate_board_values(starting_board)
    assert value_no_white_king == -999.0
