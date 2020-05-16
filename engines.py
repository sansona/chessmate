"""
Collection of chess engines that evaluate board state and select best moves
"""
import random
from helper_functions import tabulate_board_values
from constants import CONVENTIONAL_PIECE_VALUES


class ChessEngine():
    """
    Base class for defining an engine. Each engine is responsible for
    evaluating a board state and providing a move

    Attributes:
        name (str): name of engine
        legal_moves (Dict{chess.Move: float}): Dict of all current legal moves
            and value of those moves
        value_mapping (Dict{string: float}): maps type of piece to value sytem
        squares (List): python-chess doesn't allow for piece searching via.
            str. This variable maps strings to squares (see usage in
            CaptureHighestValue)

    Methods:
        get_piece_at(board, position: str) -> str: gets symbol of piece at
            specific location
        evaluate(board): unique to each engine, needs to be redefined when
            engine requires evaluation. Responsible for
            evaluating a board state based off engine criteria
        move(board): unique to each engine, needs to be redefined in each case.
            Responsible for selecting a move
            based on engine evaluation. Should return a UCI move object
    """

    def __init__(self) -> None:
        """
        Args:
            name (str): name of engine
            legal_moves (List): list of all legal moves available in
                uci notation
            value_mapping (Dict): maps type of piece to value system in
                form {piece symbol: int}
            value_differential (List[float]): difference in value on board
                at each end step
            squares (List): python-chess doesn't allow for piece searching via.
                str. This variable maps strings to squares
                (see usage in CaptureHighestValue)
        """
        self.name = None
        self.legal_moves = {}

        # Use conventional mapping for base class
        self.value_mapping = CONVENTIONAL_PIECE_VALUES
        self.value_differentials = []

        # Since python-chess doesn't provide functionality for getting piece
        # at square via. string notation, setup own board to map strings to
        # squares
        self.squares = []
        for letter in 'ABCDEFGH':
            file = [f"{letter}{r}" for r in range(1, 9)]
            self.squares.extend(file)

    def get_piece_at(self, board, position: str) -> str:
        """
        Gets chess symbol of piece at position on board

        Args:
            board (chess.board): current board state in python-chess object
            position (str):

        Returns:
            (str): symbol of piece at square
        """
        return board.piece_at(self.squares.index(position.upper())).symbol()

    def evaluate(self, board):
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
        raise NotImplementedError('Function evaluate not implemented')

    def move(self):
        """
        Selects move based on engine settings

        Raises:
            NotImplementedError: if not redefined in child class

        Returns:
            (chess.Move): uci notation object of chosen move
        """
        raise NotImplementedError('Function move not implemented')


class Random(ChessEngine):
    """ Engine that simply chooses random legal move """

    def __init__(self):
        """ See parent docstring """
        super().__init__()
        self.name = "Random"

    def evaluate(self, board):
        """ Assigns same value to each move since eventually going to choose
        random move """
        self.legal_moves = {}
        legal_move_list = list(board.legal_moves)
        self.legal_moves = {
            legal_move_list[i]: 1 for i in range(len(legal_move_list))}
        self.value_differentials.append(tabulate_board_values(board))

    def move(self, board):
        """Selects random move. See parent docstring"""
        self.evaluate(board)
        return random.choice([*self.legal_moves])


class RandomCapture(ChessEngine):
    """ Engine that prioritizes capturing any piece
    if the option presents itself """

    def __init__(self):
        """ See parent docstring """
        super().__init__()
        self.name = "Random Capture"

    def evaluate(self, board):
        """ Assigns highest value to capture moves and no value to others """
        self.legal_moves = {}

        legal_move_list = list(board.legal_moves)
        for m in legal_move_list:
            if board.is_capture(m):
                self.legal_moves[m] = 1
            else:
                self.legal_moves[m] = 0

        self.value_differentials.append(tabulate_board_values(board))

    def move(self, board):
        """Select move that features capture out of random moves
        if one is available. See parent docstring"""
        self.evaluate(board)

        # If no capture move available, return any key
        if not 1 in self.legal_moves.values():
            return list(self.legal_moves)[0]

        # Return first available capture move identified
        for m in list(self.legal_moves):
            if self.legal_moves[m] == 1:
                return m


class CaptureHighestValue(ChessEngine):
    """ Engine that prioritizes capturing the highest value piece if
    the option presents itself """

    def __init__(self):
        """ See parent docstring """
        super().__init__()
        self.name = "Capture Highest Value"

    def evaluate(self, board):
        """ Assigns highest value to capture moves based off value system """
        self.legal_moves = {}

        legal_move_list = list(board.legal_moves)
        for m in legal_move_list:
            # No value given to non-captures
            if not board.is_capture(m):
                self.legal_moves[m] = 0
            else:
                # For capture moves, assign value of piece captured to move
                try:
                    capture_val = self.value_mapping[
                        self.get_piece_at(board, str(m)[:2]).upper()]
                    self.legal_moves[m] = capture_val
                except AttributeError:
                    # Thrown by get_piece_at when no piece at square
                    self.legal_moves[m] = 0

        self.value_differentials.append(tabulate_board_values(board))

    def move(self, board):
        """Select move that features capture out of random moves
        if one is available. See parent docstring"""
        self.evaluate(board)
        highest_capture_val, highest_capture_uci = 0, None

        # Find move with highest capture value
        for m in list(self.legal_moves):
            if self.legal_moves[m] > highest_capture_val:
                highest_capture_val, highest_capture_uci = (
                    self.legal_moves[m], m)

        # If any captures available, return highest value capture. Else,
        # return random move
        if highest_capture_uci:
            return highest_capture_uci

        return list(self.legal_moves)[0]
