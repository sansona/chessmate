""" Tests for transposition table functionality """
import random

import chess  # type: ignore
import pytest  # type: ignore

from transpositions import *

# Since hashes are randomly generated, seed hashed for tests for consistency
random.seed(42)


@pytest.fixture
def known_zobrist_hash():
    """
    Setup seeded Zobrist hash table

    Returns:
        (Int): seeded starting board hash
        (List): seeded hash table
    """
    hash_table = [
        [[random.randint(1, 2 ** 64 - 1) for i in range(12)] for j in range(8)]
        for k in range(8)
    ]
    known_starting_hash = zobrist_hash_function(chess.Board(), hash_table)

    return known_starting_hash, hash_table


def test_zobrist_hash_function_starting_board(known_zobrist_hash):
    """ Tests that zobrist hash function returns correct hash
    for starting position """
    _hash = zobrist_hash_function(chess.Board(), known_zobrist_hash[1])
    assert _hash == known_zobrist_hash[0]


def test_zobrist_hash_function_changes(known_zobrist_hash):
    """ Tests that zobrist hash function changes with different
    board states i.e not the same as starting hash """
    e4_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/" "PPPP1PPP/RNBQKBNR w KQkq - 0 1"
    _hash = zobrist_hash_function(
        chess.Board(fen=e4_fen), known_zobrist_hash[1]
    )

    # Check that hash differs from starting hash value
    assert _hash != known_zobrist_hash[0]


def test_zobrist_hash_function_returns_same_value(known_zobrist_hash):
    """ Tests that zobrist hash function returns same hash value
    for each run """
    dummy_fen = (
        "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/" "PPPP1PPP/RNBQKB1R w KQkq - 0 1"
    )

    # Hash board 3 times under same conditions
    hash1 = zobrist_hash_function(
        chess.Board(fen=dummy_fen), known_zobrist_hash[1]
    )
    hash2 = zobrist_hash_function(
        chess.Board(fen=dummy_fen), known_zobrist_hash[1]
    )
    hash3 = zobrist_hash_function(
        chess.Board(fen=dummy_fen), known_zobrist_hash[1]
    )

    # Check that each hash is identical
    assert hash1 == hash2 == hash3


def test_zobrist_hash_function_different_board_different_hash(
    known_zobrist_hash,
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
        chess.Board(fen=a4_fen), known_zobrist_hash[1]
    )
    b4_hash = zobrist_hash_function(
        chess.Board(fen=b4_fen), known_zobrist_hash[1]
    )
    white_queen_e4_hash = zobrist_hash_function(
        chess.Board(fen=white_queen_e4_fen), known_zobrist_hash[1]
    )
    black_queen_e4_hash = zobrist_hash_function(
        chess.Board(fen=black_queen_e4_fen), known_zobrist_hash[1]
    )

    # Check that 4 unique hashes generated for 4 unique board positions
    assert (
        len(set([a4_hash, b4_hash, white_queen_e4_hash, black_queen_e4_hash]))
        == 4
    )


def test_zobrist_hash_function_side_invariate(known_zobrist_hash):
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
        chess.Board(fen=white_to_play_fen), known_zobrist_hash[1]
    )
    black_play_hash = zobrist_hash_function(
        chess.Board(fen=black_to_play_fen), known_zobrist_hash[1]
    )

    # Since hash should be side invariate, both hashes should be same
    assert white_play_hash == black_play_hash


def test_transposition_table_stores_zobrist_hash(known_zobrist_hash):
    """ Tests that TranspositionTable stores zobrist hash in table """
    # Initialize table w/ defined hash function
    table = TranspositionTable(zobrist_hash_function)
    table.hash_table = known_zobrist_hash[1]
    table.hash_current_board(chess.Board())

    # Check that known starting board hash evaluated to 0 and appended to table
    assert table.table == {known_zobrist_hash[0]: 0}
