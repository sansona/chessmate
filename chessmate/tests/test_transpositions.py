""" Tests for transposition table functionality """
import random

import chess  # type: ignore
import pytest  # type: ignore

from transpositions import *

# Since hashes are randomly generated, seed hashed for tests for consistency
random.seed(42)
KNOWN_ZOBRIST_STARTING_HASH = 13207708625213899933


@pytest.fixture
def zobrist_hash_table():
    """ Setup seeded Zobrist hash table """
    return [
        [[random.randint(1, 2 ** 64 - 1) for i in range(12)] for j in range(8)]
        for k in range(8)
    ]


def test_zobrist_hash_function_starting_board(zobrist_hash_table):
    """ Tests that zobrist hash function returns correct hash
    for starting position """
    _hash = zobrist_hash_function(chess.Board(), zobrist_hash_table)
    assert _hash == KNOWN_ZOBRIST_STARTING_HASH


def test_zobrist_hash_function_changes(zobrist_hash_table):
    """ Tests that zobrist hash function changes with different
    board states i.e not the same as starting hash """
    e4_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/" "PPPP1PPP/RNBQKBNR w KQkq - 0 1"
    _hash = zobrist_hash_function(chess.Board(fen=e4_fen), zobrist_hash_table)

    # Check that hash differs from starting hash value
    assert _hash != KNOWN_ZOBRIST_STARTING_HASH


def test_zobrist_hash_function_returns_same_value(zobrist_hash_table):
    """ Tests that zobrist hash function returns same hash value
    for each run """
    dummy_fen = (
        "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/" "PPPP1PPP/RNBQKB1R w KQkq - 0 1"
    )

    # Hash board 3 times under same conditions
    hash1 = zobrist_hash_function(
        chess.Board(fen=dummy_fen), zobrist_hash_table
    )
    hash2 = zobrist_hash_function(
        chess.Board(fen=dummy_fen), zobrist_hash_table
    )
    hash3 = zobrist_hash_function(
        chess.Board(fen=dummy_fen), zobrist_hash_table
    )

    # Check that each hash is identical
    assert hash1 == hash2 == hash3


def test_zobrist_hash_function_different_board_different_hash(
    zobrist_hash_table,
):
    """ Tests that zobrist hash function returns different hashes for different
    tables """
    a4_fen = "rnbqkbnr/pppppppp/8/8/P7/8/" "1PPPPPPP/RNBQKBNR w KQkq - 0 1"
    b4_fen = "rnbqkbnr/pppppppp/8/8/1P6/8/" "P1PPPPPP/RNBQKBNR w KQkq - 0 1"
    white_queen_e4_fen = (
        "rnbqkbnr/pppppppp/8/8/4Q3/8/" "PPPPPPPP/RNB1KBNR w KQkq - 0 1"
    )
    black_queen_e4_fen = (
        "rnb1kbnr/pppppppp/8/8/4q3/8/" "PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    )

    a4_hash = zobrist_hash_function(
        chess.Board(fen=a4_fen), zobrist_hash_table
    )
    b4_hash = zobrist_hash_function(
        chess.Board(fen=b4_fen), zobrist_hash_table
    )
    white_queen_e4_hash = zobrist_hash_function(
        chess.Board(fen=white_queen_e4_fen), zobrist_hash_table
    )
    black_queen_e4_hash = zobrist_hash_function(
        chess.Board(fen=black_queen_e4_fen), zobrist_hash_table
    )

    # Check that 4 unique hashes generated for 4 unique board positions
    assert (
        len(set([a4_hash, b4_hash, white_queen_e4_hash, black_queen_e4_hash]))
        == 4
    )


def test_zobrist_hash_function_side_invariate(zobrist_hash_table):
    """ Tests that same board position evaluated from both sides
    returns same hash """
    # Both FEN are of same position with opposite sides to move
    white_to_play_fen = (
        "rnbqkbnr/ppp2ppp/8/3pp3/4P3/5N2/" "PPPP1PPP/RNBQKB1R w KQkq - 0 1"
    )
    black_to_play_fen = (
        "rnbqkbnr/ppp2ppp/8/3pp3/4P3/5N2/" "PPPP1PPP/RNBQKB1R b KQkq - 0 1"
    )

    white_play_hash = zobrist_hash_function(
        chess.Board(fen=white_to_play_fen), zobrist_hash_table
    )
    black_play_hash = zobrist_hash_function(
        chess.Board(fen=black_to_play_fen), zobrist_hash_table
    )

    assert white_play_hash == black_play_hash


def test_transposition_table_stores_zobrist_hash(zobrist_hash_table):
    """ Tests that TranspositionTable stores zobrist hash in table """
    # Initialize table w/ defined hash function
    table = TranspositionTable(zobrist_hash_function)
    table.hash_table = zobrist_hash_table
    table.hash_current_board(chess.Board())
    # assert table.table == {KNOWN_ZOBRIST_STARTING_HASH: 0}
