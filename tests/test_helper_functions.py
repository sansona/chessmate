""" Test suite for assortment of helper functions """
from helper_functions import *
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


def test_piece_at_function(starting_board):
    """ Tests that piece at function returns
    value of piece at square """
    rook = get_piece_at(starting_board, "A1")
    empty_piece = get_piece_at(starting_board, "C3")

    assert rook == "R"
    assert not empty_piece


def test_tabulate_board_values(starting_board):
    """ Tests that tabulate board values function is
    properly evaluating board state """
    starting_board_value = tabulate_board_values(starting_board)
    assert starting_board_value == 0

    # Remove white king
    starting_board.remove_piece_at(chess.E1)
    no_white_king_value = tabulate_board_values(starting_board)
    assert no_white_king_value == -999.0

    # Replace white king
    starting_board.set_piece_at(chess.E1, chess.Piece(6, chess.WHITE))
    replace_white_king_value = tabulate_board_values(starting_board)
    assert replace_white_king_value == 0

    # Remove one black bishop and white queen
    starting_board.remove_piece_at(chess.C8)
    starting_board.remove_piece_at(chess.D1)
    trade_wqueen_bbishop_value = tabulate_board_values(starting_board)
    assert trade_wqueen_bbishop_value == -6.0
