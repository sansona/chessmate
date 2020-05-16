""" Helper functions """
import chess
from constants import CONVENTIONAL_PIECE_VALUES, PIECE_NAMES


def tabulate_board_values(board) -> float:
    """
    Iterate through board, and determine net piece value difference

    Args:
        board (chess.Board)

    Returns:
        (float): containing net value difference
    """
    value_difference = 0.0

    # Go through each square, find piece at square, add value to
    # value_difference
    for square in chess.SQUARES:
        piece = board.piece_type_at(square)
        color = board.color_at(square)
        if piece:
            value = CONVENTIONAL_PIECE_VALUES[PIECE_NAMES[piece]]
            if not color:
                # BLACK encoded as False
                value *= -1
            value_difference += value

    return value_difference
