""" Collection of heuristic related evaluation - move sorting,
board evaluation """
from typing import List, Dict
import chess
from pprint import pprint

from utils import get_piece_at
from constants.piece_values import CONVENTIONAL_PIECE_VALUES


def MVV_LVA(
    board: chess.Board,
    piece_values: Dict[str, int] = CONVENTIONAL_PIECE_VALUES,
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
            value_diff = (
                piece_values[victim_piece] - piece_values[aggressor_piece]
            )

            if value_diff not in available_captures:
                available_captures[value_diff] = [move]
            else:
                available_captures[value_diff].append(move)

    move_list_sorted = []
    for val_diff in sorted(available_captures, reverse=True):
        move_list_sorted.extend(available_captures[val_diff])

    if move_list_sorted:
        return move_list_sorted
    # If no captures, return unsorted list of all legal moves
    return move_list


board = chess.Board(
    fen="rnb1k2r/pppppppp/8/2q5/1P2bn2/3N1PP1/P1PPP2P/R1BQKBNR w KQkq - 0 1"
)
pprint(MVV_LVA(board))
