""" Functions for analyzing board states and results of games """
from typing import Dict

import numpy as np
import chess

from utils import get_piece_value_from_table
from constants.piece_values import (
    CONVENTIONAL_PIECE_VALUES,
    PIECE_TABLE_CONVENTIONAL,
)
from constants.misc import PIECE_NAMES


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


class EvaluationFunction:
    """
    Base class for board evaluation algorithms. Each EvaluationFunction
    object is responsible for evaluating a given boardstate and
    returning a numeric metric from its evaluation. Standard for metric
    wherein positive evaluations are pro-white and negative pro-black

    Every evaluation performed by the engine should be stored in the
    evaluations attribute

    Attributes:
        name (str): name of evaluation engine
        evaluations (Dict[str, float]): stores each board
            state evaluated as FEN and the corresponding metric
        piece_values (Dict[str, float]): mapping of pieces to values.
            By default use conventional piece values

    Methods:
        evaluate (chess.Board) -> float: main function responsible for
            evaluation of board state
    """

    def __init__(self):
        self.name: str = "Base"
        self.evaluations: Dict[str, float] = {}
        self.piece_values: Dict[str, float] = CONVENTIONAL_PIECE_VALUES

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


class StandardEvaluation(EvaluationFunction):
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
                piece_value = self.piece_values[PIECE_NAMES[piece]]
                if not color:
                    # BLACK encoded as False
                    piece_value *= -1
                val += piece_value
        self.evaluations[board.fen()] = val

        return val


class PieceValueEvaluation(EvaluationFunction):
    """ Evaluation engine that utilizes piece value tables
    to evaluate position of piece in addition to defined values

    Note that since the evaluate function requires a large number of iterations,
    this implementation is computationally slow

    Attributes:
        value_tables (Dict[str, np.ndarray]: defined collection of piece
            value tables. Default to conventional piece table
    """

    def __init__(self):
        """ See parent docstring """
        super().__init__()
        self.name = "PieceValue"
        self.value_tables: Dict[str, np.ndarray] = PIECE_TABLE_CONVENTIONAL

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
                piece_value = get_piece_value_from_table(
                    PIECE_NAMES[piece], color, square, self.value_tables
                )
                val += piece_value
        self.evaluations[board.fen()] = val

        return val
