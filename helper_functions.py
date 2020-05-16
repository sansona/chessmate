""" Helper functions """
from constants import SQUARE_STR, CONVENTIONAL_PIECE_VALUES, PIECE_NAMES
import chess


def get_piece_at(board, position: str) -> str:
    """
    Gets chess symbol of piece at position on board

    Args:
        board (chess.board): current board state in python-chess object
        position (str):

    Raises:
        AttributeError: if no piece on board at position

    Returns:
        (str): symbol of piece at square if any
    """
    try:
        return board.piece_at(SQUARE_STR.index(position.upper())).symbol()
    except AttributeError:
        return ""


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


def display_pgn(pgn_game):
    """
    Displays game loaded from pgm
    Args:
        pgn_game (chess.png.game)
    """
    pgn = StringIO(str(pgn_game))
    game = chess.pgn.read_game(pgn)
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
        print(f"{board}\n")
