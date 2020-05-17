""" Utility functions """
from constants import SQUARE_STR, CONVENTIONAL_PIECE_VALUES, PIECE_NAMES
from io import StringIO
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


def display_pgn_text(pgn_game):
    """
    Displays game loaded from pgn in text form
    Args:
        pgn_game (chess.png.game)
    """
    pgn = StringIO(str(pgn_game))
    game = chess.pgn.read_game(pgn)
    board = game.board()
    move_count = 1
    for move in game.mainline_moves():
        mover = "White" if move_count % 2 == 0 else "Black"
        board.push(move)
        print(f"Move: {move_count}. {mover} to move")
        print(f"{board}\n")
        print("---------------")
        move_count += 1


def display_pgn_svg(pgn_game):
    """
    Displays game loaded from pgn in svg. Designed for
    use in jupyter notebooks as generator
    Args:
        pgn_game (chess.png.game)
    """
    pgn = StringIO(str(pgn_game))
    game = chess.pgn.read_game(pgn)
    board = game.board()
    move_count = 1
    for move in game.mainline_moves():
        mover = "White" if move_count % 2 == 0 else "Black"
        board.push(move)
        print(f"Move: {move_count}. {mover} to move")
        move_count += 1
        yield board
