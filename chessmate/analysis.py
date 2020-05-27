""" Functions for analyzing board states and results of games """
from typing import Dict

import chess

from constants import CONVENTIONAL_PIECE_VALUES, PIECE_NAMES


def evaluate_ending_board(board: chess.Board) -> str:
    """
    Determines conditions leading to end of game

    Args:
        board (chess.Board)
    Returns:
        (str): designating condition of game ending
    """
    result = board.result()

    if not board.is_game_over():
        return "Game over by resignation"
    if result == "1-0":
        return "White win by mate"
    if result == "0-1":
        return "Black win by mate"

    # A different design pattern may be to move this var to the init
    # so as to not keep initializing it on each call, but I want to
    # explicitly initialize it on each call since it's dependent on
    # the current board state
    terminal_conditions = {
        "Checkmate": board.is_checkmate,
        "Stalemate": board.is_stalemate,
        "Insufficient material": board.is_insufficient_material,
        "Seventyfive moves": board.is_seventyfive_moves,
        "Fivefold repetition": board.is_fivefold_repetition,
    }

    for title, condition in terminal_conditions.items():
        if condition():
            return title

    # If none of the defined ending states found, game ended due to
    # some variable endstate that would require further probing.
    # This would be the case if playing some variation
    return "Undetermined"


class BoardEvaluation:
    """
    Base class for board evaluation algorithms. Each BoardEvaluation
    object is responsible for evaluating a given boardstate and
    returning a numeric metric from its evaluation. Standard for metric
    wherein positive evaluations are pro-white and negative pro-black

    Every evaluation performed by the engine should be stored in the
    evaluations attribute

    Attributes:
        name (str): name of evaluation engine
        evaluations (Dict[str, float]): stores each board
            state evaluated as FEN and the corresponding metric

    Methods:
        evaluate (chess.Board) -> float: main function responsible for
            evaluation of board state
    """

    def __init__(self):
        self.name: str = "Base"
        self.evaluations: Dict[str, float] = {}

    def evaluate(self, board: chess.Board) -> float:
        """
        Main function for evaluating given boardstate. Function should
        evaluate boardstate and append evaluation in evaluations

        Args:
            board (chess.Board): board state to evaluate
        Returns:
            (float)
        """
        raise NotImplementedError("Function evaluate not implemented")


class StandardEvaluation(BoardEvaluation):
    """ Evaluation engine that tabulates value of all pieces on both
    sides according to the standard piece valuation and calculates
    difference as metric """

    def __init__(self):
        """ See parent docstring """
        super().__init__()
        self.name = "Standard"

    def evaluate(self, board: chess.Board) -> float:
        """
        Main function for evaluating given boardstate. Function should
        evaluate boardstate and append evaluation in evaluations

        Args:
            board (chess.Board): board state to evaluate
        Returns:
            (float)
        """
        val = 0.0
        for square in chess.SQUARES:
            piece = board.piece_type_at(square)
            color = board.color_at(square)
            if piece:
                piece_value = CONVENTIONAL_PIECE_VALUES[PIECE_NAMES[piece]]
                if not color:
                    # BLACK encoded as False
                    piece_value *= -1
                val += piece_value
        self.evaluations[board.fen()] = val

        return val
