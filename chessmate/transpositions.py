""" Functions related to hash_tableing and transposition tables """
import random
from typing import List
import chess

from analysis import StandardEvaluation
from utils import get_piece_at
from constants.misc import PIECE_INDEXING


def zobrist_hash_function(board: chess.Board, hash_table: List) -> int:
    """
    Hashes board according to Zobrist hash schema

    Args:
        board (chess.Board): boardstate
        hash_table (List): randomly generated hash table

    Returns:
        (int): hashed board
    """
    _hash = 0
    for square in chess.SQUARES:
        piece = get_piece_at(board=board, position=square)
        # If piece on square, hash piece based off piece identity and position
        if piece:
            piece_idx = PIECE_INDEXING[piece]
            rank, _file = chess.square_rank(square), chess.square_file(square)
            # Bitwise XOR on _hash
            _hash ^= hash_table[rank][_file][piece_idx]

    return _hash


def BCH_hash_function(board: chess.Board, hash_table: List) -> int:
    """
    Hashes board according to BCH hash schema

    Args:
        board (chess.Board): boardstate
        hash_table (List): randomly generated hash table

    Returns:
        (int): hashed board
    """
    pass


class TranspositionTable:
    """
    Base class for transposition tables
    """

    def __init__(self, hash_function):
        self.hash_function = hash_function
        self.hash_table = [
            [
                [random.randint(1, 2 ** 64 - 1) for i in range(12)]
                for j in range(8)
            ]
            for k in range(8)
        ]
        self.evaluation_function = StandardEvaluation
        self.table = {}

    def hash_position(self, board: chess.Board):
        """
        Wrapper for hashing boardstate

        Args:
            board (chess.Board): board state

        Returns:
            (int)
        """
        return self.hash_function(board, self.hash_table)

    def append_boardstate_to_table(self, board: chess.Board):
        """
        Adds hashed boardstate to table with evaluation
 
        Args:
            board (chess.Board): board state
        """
        pass
