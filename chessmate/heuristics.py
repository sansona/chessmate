""" Collection of heuristic related evaluation - move sorting,
board evaluation """
import random
from typing import Dict, List

import chess  # type: ignore

from chessmate.constants.piece_values import ConventionalPieceValues
from chessmate.utils import get_piece_at


def MVV_LVA(
    board: chess.Board, piece_values: Dict[str, int] = ConventionalPieceValues
) -> List[chess.Move]:
    """
    Most Valuable Victim - Least Valuable Aggressor implementation for
    move sorting

    Args:
        board (chess.Board): current board state to evaluate
    Returns:
        (List[chess.Move]): sorted list of moves according to MVV_LVA capture
            heuristic
    """
    available_captures: Dict[int, List[chess.Move]] = {}
    move_list = list(board.legal_moves)
    # For each move, evaluate if any captures. If so, rank captures based
    # off value gained
    for move in move_list:
        if board.is_capture(move):
            # Get difference in value between aggressor and victim pieces
            aggressor_piece = get_piece_at(board, str(move)[:2]).upper()
            victim_piece = get_piece_at(board, str(move)[2:]).upper()
            if aggressor_piece and victim_piece:
                value_diff = (
                    piece_values[victim_piece].value
                    - piece_values[aggressor_piece].value
                )

                if value_diff not in available_captures:
                    available_captures[value_diff] = [move]
                else:
                    available_captures[value_diff].append(move)

    # If any available captures, sort captures by value_diff of captures
    # and return list of sorted captures
    if available_captures:
        move_list_sorted = []
        for val_diff in sorted(available_captures, reverse=True):
            move_list_sorted.extend(available_captures[val_diff])
        return move_list_sorted

    # If no captures, return shuffled list of all legal moves
    random.shuffle(move_list)
    return move_list
