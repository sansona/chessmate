""" Collection of tests for heuristics """
import chess
import pytest

from heuristics import *
from constants.piece_values import (
    CONVENTIONAL_PIECE_VALUES,
    FISCHER_PIECE_VALUES,
)


def test_mvv_lva_conventional_returns_sorted_captures():
    """ Tests that MVV_LVA with conventional piece values returns all captures
    sorted by highest value difference """

    white_aggressor_fen = (
        "rnb1k2r/pppppppp/8/2q5/1P2bn2" "/3N1PP1/P1PPP2P/R1BQKBNR w KQkq - 0 1"
    )
    board = chess.Board(fen=white_aggressor_fen)

    # All available captures in fen position sorted
    pawn_capture_queen = chess.Move.from_uci("b4c5")
    knight_capture_queen = chess.Move.from_uci("d3c5")
    pawn_capture_knight = chess.Move.from_uci("g3f4")
    pawn_capture_bishop = chess.Move.from_uci("f3e4")
    knight_capture_knight = chess.Move.from_uci("d3f4")
    captures_sorted = [
        pawn_capture_queen,
        knight_capture_queen,
        pawn_capture_knight,
        pawn_capture_bishop,
        knight_capture_knight,
    ]

    assert MVV_LVA(board, CONVENTIONAL_PIECE_VALUES) == captures_sorted


def test_mvv_lva_fischer_returns_sorted_captures():
    """ Tests that MVV_LVA with Fischer piece values (where bishop is ranked
    higher than knight returns captures with bishops prioritized over knights
    """
    white_capture_bishop_or_knight_fen = (
        "rnbqk2r/pppppppp/8/8/3bn3/" "2P2P2/PP1PP1PP/RNBQKBNR w KQkq - 0 1"
    )
    board = chess.Board(fen=white_capture_bishop_or_knight_fen)

    pawn_capture_bishop = chess.Move.from_uci("c3d4")
    pawn_capture_knight = chess.Move.from_uci("f3e4")

    # Since Fischer values rank bishop over knight, should prioritize bishop
    captures_sorted = [pawn_capture_bishop, pawn_capture_knight]

    assert MVV_LVA(board, FISCHER_PIECE_VALUES) == captures_sorted


def test_mvv_lva_no_captures_returns_random_sorted():
    """ Tests that MVV_LVA returns a randomly sorted list of legal moves if
    given board with no available captures """
    board = chess.Board()
    legal_move_list = list(board.legal_moves)
    # To check whether random list generated from MVV_LVA, check that
    # lists are not identical but when sorted are
    assert MVV_LVA(board) != legal_move_list
    assert set(MVV_LVA(board)) == set(legal_move_list)
