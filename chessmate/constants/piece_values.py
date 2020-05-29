""" Repository for piece value constants used across library """
import numpy as np

CONVENTIONAL_PIECE_VALUES = {
    "P": 100,
    "N": 350,
    "B": 350,
    "R": 525,
    "Q": 1000,
    "K": 99999,
}

# Convention for piece tables is each rank in own array.
# NOTE: to access a specific file and rank, use table[rank][file]
# NOTE: the piece values are from the perspective of white i.e
# table[0] corresponds to rank 1. In short, A1 = table[0][0]
PAWN_PIECE_TABLE_CONVENTIONAL = np.array(
    [
        [0] * 8,
        [5, 10, 10, -20, -20, 10, 10, 5],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50] * 8,
        [0] * 8,
    ]
)

KNIGHT_PIECE_TABLE_CONVENTIONAL = np.array(
    [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-30, 5, 10, 15, 15, 1, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 1, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50],
    ]
)

BISHOP_PIECE_TABLE_CONVENTIONAL = np.array(
    [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 0, 10, 10, 10, 5, 5, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20],
    ]
)

ROOK_PIECE_TABLE_CONVENTIONAL = np.array(
    [
        [0, 0, 0, 5, 5, 0, 0, 0],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [0] * 8,
    ]
)

QUEEN_PIECE_TABLE_CONVENTIONAL = np.array(
    [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [-10, 0, 5, 5, 5, 0, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20],
    ]
)

KING_PIECE_TABLE_CONVENTIONAL = np.array(
    [
        [20, 30, 10, 0, 0, 10, 30, 20],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
    ]
)

PIECE_TABLE_CONVENTIONAL = {
    "P": PAWN_PIECE_TABLE_CONVENTIONAL,
    "N": KNIGHT_PIECE_TABLE_CONVENTIONAL,
    "B": BISHOP_PIECE_TABLE_CONVENTIONAL,
    "R": ROOK_PIECE_TABLE_CONVENTIONAL,
    "Q": QUEEN_PIECE_TABLE_CONVENTIONAL,
    "K": KING_PIECE_TABLE_CONVENTIONAL,
}
