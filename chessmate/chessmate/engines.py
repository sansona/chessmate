"""
Collection of chess engines that evaluate board state and select best moves
"""
import random
from typing import Dict, List, Union

import chess  # type: ignore
import chess.pgn  # type: ignore

from analysis import tabulate_board_values
from constants import CONVENTIONAL_PIECE_VALUES
from utils import get_piece_at


class BaseEngine:
    """
    Base class for defining an engine. Each engine is responsible for
    evaluating a board state and providing a move

    Attributes:
        name (str): name of engine
        legal_moves (Dict{chess.Move: float}): Dict of all current legal moves
                and value of those moves
        value_mapping (Dict{string: float}): maps type of piece to value sytem

    Methods:
        evaluate(board): unique to each engine, needs to be redefined when
            engine requires evaluation. Responsible for
            evaluating a board state based off engine criteria
        move(board): unique to each engine, needs to be redefined in each case.
            Responsible for selecting a move
            based on engine evaluation. Should return a UCI move object
        reset_move_variables(): reinitialize variables for beginning of move
            evaluation
        reset_game_variables(): reinitialize variables for beginning of new
            game
    """

    def __init__(self) -> None:
        """
        Args:
            name (str): name of engine
            legal_moves (Dict[chess.Move, float]): list of all legal moves
                available in uci notation with values for each move
            value_mapping (Dict): maps type of piece to value system in
                form {piece symbol: int}. Use conventional values by default
            material_difference (List[float]): difference in value on board
                at each end step based off material
        """
        self.name: str = "Base"
        self.legal_moves: Dict[chess.Move, float] = {}
        self.value_mapping: Dict[str, float] = CONVENTIONAL_PIECE_VALUES
        self.material_difference: List[float] = []

    def __repr__(self):
        """ Print out current state of engine """
        return f"""name: {self.name}
                legal_moves: {self.legal_moves}
                value mapping: {self.value_mapping}
                material difference: {self.material_difference}"""

    def evaluate(self, board: chess.Board) -> None:
        """
        Evaluates current board state and returns values of different moves

        Args:
            board (chess.board): current board state in python-chess object

        Raises:
            NotImplementedError: if not redefined in child class

        Returns:
            (Dict[chess.Move: float]): dict mapping uci moves to
                evaluated value metric
        """
        raise NotImplementedError("Function evaluate not implemented")

    def move(self, board: chess.Board) -> chess.Move:
        """
        Selects move based on engine settings

        Args:
            board (chess.board): current board state in python-chess object

        Raises:
            NotImplementedError: if not redefined in child class

        Returns:
            (chess.Move): uci notation object of chosen move
        """
        raise NotImplementedError("Function move not implemented")

    def reset_move_variables(self) -> None:
        """ Resets variables at end of move"""
        self.legal_moves = {}

    def reset_game_variables(self) -> None:
        """ Resets variables at end of game"""
        self.material_difference = []


class Random(BaseEngine):
    """ Engine that simply chooses random legal move """

    def __init__(self):
        """ See parent docstring """
        super().__init__()
        self.name = "Random"

    def evaluate(self, board: chess.Board) -> None:
        """ Assigns same value to each move since eventually going to choose
        random move """
        self.reset_move_variables()

        legal_move_list = list(board.legal_moves)
        self.legal_moves = {
            legal_move_list[i]: 1 for i in range(len(legal_move_list))
        }
        self.material_difference.append(tabulate_board_values(board))

    def move(self, board: chess.Board) -> chess.Move:
        """Selects random move. See parent docstring"""
        self.evaluate(board)

        # If no legal moves available, return null move and pass turn
        # so that board.is_game_over() is flagged
        if not [*self.legal_moves]:
            return chess.Move.null()

        return random.choice([*self.legal_moves])


class PrioritizePawnMoves(Random):
    """ Engine that only moves pawns when an option. Default to random
    engines if no pawn moves available"""

    def __init__(self):
        """ See parent docstring """
        super().__init__()
        self.name = "Prioritize Pawn Moves"

    def evaluate(self, board: chess.Board) -> None:
        """ Assigns same value to each move since eventually going to choose
        random move """
        self.reset_move_variables()

        legal_move_list = list(board.legal_moves)
        for m in legal_move_list:
            if get_piece_at(board, str(m)[:2].upper()) == "P":
                self.legal_moves[m] = 1

        # If no pawn moves available, all moves are same priority
        if not self.legal_moves:
            self.legal_moves = {
                legal_move_list[i]: 1 for i in range(len(legal_move_list))
            }

        self.material_difference.append(tabulate_board_values(board))


class RandomCapture(BaseEngine):
    """ Engine that prioritizes capturing any piece
    if the option presents itself """

    def __init__(self):
        """ See parent docstring """
        super().__init__()
        self.name = "Random Capture"

    def evaluate(self, board: chess.Board) -> None:
        """ Assigns highest value to capture moves and no value to others """
        self.reset_move_variables()

        legal_move_list = list(board.legal_moves)
        for m in legal_move_list:
            if board.is_capture(m):
                self.legal_moves[m] = 1
            else:
                self.legal_moves[m] = 0

        self.material_difference.append(tabulate_board_values(board))

    def move(self, board: chess.Board) -> chess.Move:
        """Select move that features capture out of random moves
        if one is available. See parent docstring"""
        self.evaluate(board)

        if not [*self.legal_moves]:
            return chess.Move.null()

        # If no capture move available, return any key
        if 1 not in self.legal_moves.values():
            return random.choice([*self.legal_moves])

        # Return first available capture move identified
        for m in list(self.legal_moves):
            if self.legal_moves[m] == 1:
                return m


class CaptureHighestValue(BaseEngine):
    """ Engine that prioritizes capturing the highest value piece if
    the option presents itself """

    def __init__(self):
        """ See parent docstring """
        super().__init__()
        self.name = "Capture Highest Value"

    def evaluate(self, board: chess.Board) -> None:
        """ Assigns highest value to capture moves based off value system """
        self.reset_move_variables()

        legal_move_list = list(board.legal_moves)
        for m in legal_move_list:
            piece_at_position = get_piece_at(board, str(m)[2:4]).upper()

            if (not board.is_capture(m)) or (not piece_at_position):
                self.legal_moves[m] = 0.0
            else:
                self.legal_moves[m] = self.value_mapping[piece_at_position]

        self.material_difference.append(tabulate_board_values(board))

    def move(self, board: chess.Board) -> chess.Move:
        """Select move that features capture out of random moves
        if one is available. See parent docstring"""
        self.evaluate(board)

        if not [*self.legal_moves]:
            return chess.Move.null()

        highest_capture_val, highest_capture_uci = 0.0, None

        # Find move with highest capture value
        for m in list(self.legal_moves):
            if self.legal_moves[m] > highest_capture_val:
                highest_capture_val, highest_capture_uci = (
                    self.legal_moves[m],
                    m,
                )

        # If any captures available, return highest value capture. Else,
        # return random move
        if highest_capture_uci:
            return highest_capture_uci
        return random.choice([*self.legal_moves])


class AvoidCapture(RandomCapture):
    """ Engine that prioritizes NOT capturing a piece whenver possible """

    def __init__(self):
        """ See parent docstring """
        super().__init__()
        self.name = "Avoid Capture"

    def evaluate(self, board: chess.Board) -> None:
        """ Assigns value to no capture moves and no value to captures """
        self.reset_move_variables()

        legal_move_list = list(board.legal_moves)
        # The only difference between this engine and RandomCapture is the
        # not condition.
        for m in legal_move_list:
            if not board.is_capture(m):
                self.legal_moves[m] = 1
            else:
                self.legal_moves[m] = 0

        self.material_difference.append(tabulate_board_values(board))


class ScholarsMate(BaseEngine):
    """ Engine that only executes scholar's mate. Note that since
    scholar's mate is defined for white play, engine will forfeit
    is on black side. """

    def __init__(self):
        """ See parent docstring """
        super().__init__()
        self.name = "Scholar's Mate"

    def evaluate(self, board: chess.Board) -> None:
        """ Inits scholar's mate play as legal_moves """
        self.reset_move_variables()

        moves = ("e2e4", "f1c4", "d1h5", "h5f7")
        for m in moves:
            self.legal_moves[m] = 0

        self.material_difference.append(tabulate_board_values(board))

    def move(self, board: chess.Board) -> chess.Move:
        """ Run through scholar's mate sequence. If any moves become
        blocked, resign """

        # Since Scholar's Mate relies on standard board setup, resign
        # if starting board is not standard
        if (board.fullmove_number == 1) and (
            board.starting_fen != chess.STARTING_FEN
        ):
            return chess.Move.null()

        self.evaluate(board)

        # If past first five moves, resign
        if board.fullmove_number not in range(1, 5):
            return chess.Move.null()

        # If any of scholar's mate moves blocked, resign
        move = [*self.legal_moves][board.fullmove_number - 1]

        if move not in [str(m) for m in list(board.legal_moves)]:
            return chess.Move.null()

        return chess.Move.from_uci(move)


class MiniMax(BaseEngine):
    """
    Base class for engines utilizing the MiniMax algorithm. Inherits from
    BaseEngine.

    Attributes:
        name (str): name of engine
        color (Union[chess.Color, bool]): color for MiniMax to evaluate board
            from
        depth (int): number of child nodes to traverse in algorithm
        best_move (chess.Move): move evaluated as best by minimax algorithm.
            Default to null
        alpha_beta_pruning (bool): if want to prune trees. Default=True
        alpha (float): alpha value in pruning, default=-inf
        beta (float): beta value in pruning, default= inf

    Methods:
        minimax(base_board, maximizing, depth): main algorithmic loop for
            minimax algorithm.
    """

    def __init__(self, color: Union[chess.Color, bool], depth: int):
        super().__init__()
        self.name = "MiniMax"
        self.color: Union[chess.Color, bool] = color
        self._depth: int = depth
        self.best_move: chess.Move = chess.Move.null()
        self.alpha_beta_pruning: bool = True
        self.alpha: float = float("-inf")
        self.beta: float = float("inf")

    @property
    def depth(self) -> int:
        """ Getter for depth """
        return self._depth

    @depth.setter
    def depth(self, depth_val: int) -> None:
        """
        Setter for setting new depth after initialzation with new fen

        Args:
            depth_val (int)

        Raise:
            TypeError: if non-int depth set
        """
        if not isinstance(depth_val, int):
            raise TypeError(f"depth {depth_val} of type {type(depth_val)}")
        self._depth = depth_val

    def minimax(
        self,
        base_board: chess.Board,
        maximizing: bool,
        depth: int,
        alpha: float,
        beta: float,
    ) -> float:
        """
        Evaluate result of each legal move on board via. minimax algorithm
        Reference: https://www.youtube.com/watch?v=l-hh51ncgDI

        Args:
            base_board (chess.Board): current board state
            maximizing (bool): True for white, False for black
            depth (int): depth to search. Init at self._depth for base. Note:
                    depth=>3 will be computationally slow for most CPUs
        """
        if depth == 0 or base_board.is_game_over():
            return tabulate_board_values(base_board)

        # Evaluate position after each legal move, store result of
        # best move
        if maximizing:
            max_val = -float("inf")
            # Shuffle moves to prevent move ordering from impacting game
            # results
            legal_moves = list(base_board.legal_moves)
            random.shuffle(legal_moves)
            for move in legal_moves:
                base_board.push_uci(str(move))
                val = self.minimax(base_board, False, depth - 1, alpha, beta)
                popped_move = base_board.pop()

                if val > max_val:
                    max_val = val
                    # Keep only best moves for own color and at the root of
                    # the move tree corresponding to the best move
                    if (self.color) and (depth == self._depth):
                        self.best_move = popped_move

                if self.alpha_beta_pruning:
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        break

            return max_val

        # elif not strictly necessary but increasing readability
        elif not maximizing:
            min_val = float("inf")
            legal_moves = list(base_board.legal_moves)
            random.shuffle(legal_moves)

            for move in legal_moves:
                base_board.push_uci(str(move))
                val = self.minimax(base_board, True, depth - 1, alpha, beta)
                popped_move = base_board.pop()
                if val < min_val:
                    min_val = val
                    if (not self.color) and (depth == self._depth):
                        self.best_move = popped_move
                if self.alpha_beta_pruning:
                    beta = min(beta, val)
                    if beta <= alpha:
                        break

            return min_val

    def evaluate(self, board: chess.Board) -> None:
        """ Evaluates board from perspective of side playing on """
        if isinstance(self.color, bool):
            self.minimax(
                board,
                self.color,
                depth=self._depth,
                alpha=self.alpha,
                beta=self.beta,
            )
        else:
            raise ValueError(
                f"self.color value {self.color} not in (White, Black)"
            )

        self.material_difference.append(tabulate_board_values(board))

    def move(self, board: chess.Board) -> chess.Move:
        """ Returns best move as selected by minimax algorithm """
        self.evaluate(board)
        return self.best_move