""" Test suite for assortment of analysis functions """
import sys

import chess
import chess.pgn
import pytest

from analysis import *
from engines import ScholarsMate
from simulations import ChessPlayground

sys.path.append("..")


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
def setup_playground():
    """
    Sets up test playground with 3 games played

    Returns:
            (ChessPlaygound)
    """
    playground = ChessPlayground(ScholarsMate(), ScholarsMate())
    playground.play_multiple_games(3)
    return playground


def test_evaluate_ending_not_mated(not_mated_boards):
    """ Tests that boards ending in resignation are correctly evaluated """
    for board in not_mated_boards:
        assert evaluate_ending_board(board) == "Game over by resignation"


def test_evaluate_ending_stalemate(stalemate_boards):
    """ Tests that boards ending in stalemate are correctly evaluated """
    for board in stalemate_boards:
        assert evaluate_ending_board(board) == "Stalemate"


def test_display_all_results(setup_playground):
    """ Tests that display_all_results runs """
    display_all_results(setup_playground.all_results)


def test_display_material_difference(setup_playground):
    """ Tests that display_material_difference runs """
    display_material_difference(setup_playground.all_material_differences, 0)
    display_material_difference(setup_playground.all_material_differences, 1)


def test_display_all_material_differences(setup_playground):
    """ Tests that all_display_material_difference runs """
    display_all_material_differences(setup_playground.all_material_differences)
