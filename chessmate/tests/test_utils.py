""" Test suite for assortment of helper functions """
import sys

import chess
import chess.pgn
import pytest

from analysis import StandardEvaluation
from engines import ScholarsMate
from simulations import ChessPlayground
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


@pytest.fixture
def setup_playground():
    """
    Sets up test playground with 3 games played

    Returns:
            (ChessPlaygound)
    """
    playground = ChessPlayground(ScholarsMate(), ScholarsMate())
    playground.play_multiple_games(3)
    return playground


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


def test_display_all_results_no_errors(setup_playground):
    """ Tests that display_all_results runs. Since this function
    displays in IPython console, having it run w/o errors is
    sufficient. """
    display_all_results(setup_playground.all_results)


def test_display_material_difference_no_errors(setup_playground):
    """ Tests that display_material_difference runs. Since this function
    displays in IPython console, having it run w/o errors is
    sufficient. """
    display_material_difference(setup_playground.all_material_differences, 0)
    display_material_difference(setup_playground.all_material_differences, 1)


def test_display_all_material_differences_no_errors(setup_playground):
    """ Tests that all_display_material_difference runs. Since this function
    displays in IPython console, having it run w/o errors is
    sufficient."""
    display_all_material_differences(setup_playground.all_material_differences)
