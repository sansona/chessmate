"""
Collection of chess engines that evaluate board state and select best moves
"""
import random
from analysis import tabulate_board_values
from utils import get_piece_at
from constants import CONVENTIONAL_PIECE_VALUES


class BaseEngine():
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
            legal_moves (List): list of all legal moves available in
                uci notation
            value_mapping (Dict): maps type of piece to value system in
                form {piece symbol: int}. Use conventional values by default
            material_difference (List[float]): difference in value on board
                at each end step based off material
        """
        self.name = None
        self.legal_moves = {}
        self.value_mapping = CONVENTIONAL_PIECE_VALUES
        self.material_difference = []

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

    def move(self, board):
        """
        Selects move based on engine settings

        Args:
            board (chess.board): current board state in python-chess object

        Raises:
            NotImplementedError: if not redefined in child class

        Returns:
            (chess.Move): uci notation object of chosen move
        """
        raise NotImplementedError('Function move not implemented')

    def reset_move_variables(self):
        """ Resets variables at end of move"""
        self.legal_moves = {}

    def reset_game_variables(self):
        """ Resets variables at end of game"""
        self.material_difference = []


class Random(BaseEngine):
    """ Engine that simply chooses random legal move """

    def __init__(self):
        """ See parent docstring """
        super().__init__()
        self.name = "Random"

    def evaluate(self, board):
        """ Assigns same value to each move since eventually going to choose
        random move """
        self.reset_move_variables()

        legal_move_list = list(board.legal_moves)
        self.legal_moves = {
            legal_move_list[i]: 1 for i in range(len(legal_move_list))}
        self.material_difference.append(tabulate_board_values(board))

    def move(self, board):
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

    def evaluate(self, board):
        """ Assigns same value to each move since eventually going to choose
        random move """
        self.reset_move_variables()

        legal_move_list = list(board.legal_moves)
        for m in legal_move_list:
            if get_piece_at(board, str(m)[:2].upper()) == 'P':
                self.legal_moves[m] = 1

        # If no pawn moves available, all moves are same priority
        if not self.legal_moves:
            self.legal_moves = {
                legal_move_list[i]: 1 for i in range(len(legal_move_list))}

        self.material_difference.append(tabulate_board_values(board))


class RandomCapture(BaseEngine):
    """ Engine that prioritizes capturing any piece
    if the option presents itself """

    def __init__(self):
        """ See parent docstring """
        super().__init__()
        self.name = "Random Capture"

    def evaluate(self, board):
        """ Assigns highest value to capture moves and no value to others """
        self.reset_move_variables()

        legal_move_list = list(board.legal_moves)
        for m in legal_move_list:
            if board.is_capture(m):
                self.legal_moves[m] = 1
            else:
                self.legal_moves[m] = 0

        self.material_difference.append(tabulate_board_values(board))

    def move(self, board):
        """Select move that features capture out of random moves
        if one is available. See parent docstring"""
        self.evaluate(board)

        if not [*self.legal_moves]:
            return chess.Move.null()

        # If no capture move available, return any key
        if not 1 in self.legal_moves.values():
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

    def evaluate(self, board):
        """ Assigns highest value to capture moves based off value system """
        self.reset_move_variables()

        legal_move_list = list(board.legal_moves)
        for m in legal_move_list:
            piece_at_position = get_piece_at(board, str(m)[2:4]).upper()

            if (not board.is_capture(m)) or (not piece_at_position):
                self.legal_moves[m] = 0
            else:
                self.legal_moves[m] = self.value_mapping[piece_at_position]

        self.material_difference.append(tabulate_board_values(board))

    def move(self, board):
        """Select move that features capture out of random moves
        if one is available. See parent docstring"""
        self.evaluate(board)

        if not [*self.legal_moves]:
            return chess.Move.null()

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
        return random.choice([*self.legal_moves])


class AvoidCapture(RandomCapture):
    """ Engine that prioritizes NOT capturing a piece whenver possible """

    def __init__(self):
        """ See parent docstring """
        super().__init__()
        self.name = "Avoid Capture"

    def evaluate(self, board):
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
