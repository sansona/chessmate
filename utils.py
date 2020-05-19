""" Utility functions """
import time
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from IPython.display import SVG, display, clear_output
import chess
from constants import SQUARE_STR


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


def display_pgn_text(pgn_obj) -> None:
    """
    Displays game loaded from pgn in text form

    Args:
        pgn_obj (chess.png.game)
    """
    pgn_io = StringIO(str(pgn_obj))
    game = chess.pgn.read_game(pgn_io)
    board = game.board()
    move_count = 1
    for move in game.mainline_moves():
        mover = "White" if move_count % 2 == 0 else "Black"
        board.push(move)
        print(f"Move: {move_count}. {mover} to move")
        print(f"{board}\n")
        print("---------------")
        move_count += 1


def render_svg_board(board, temp_dir, display_str):
    """
    Renders board as svg object for displaying in jupyter notebook.
    Saves board state as SVG file and displays in jupyter

    Args:
        board (chess.Board)
        temp_dir (str/Path): path to temporary directory to store
            image files in
        display_str (str): string to display alongside board for
            context
    """
    boardsvg = chess.svg.board(board=board)

    # Store each move as image in temp
    fpath = Path(temp_dir) / f"{display_str}.SVG"
    with open(fpath, "w") as f:
        f.write(boardsvg)

    display(SVG(str(fpath)))
    print(fpath.stem)
    clear_output(wait=True)


def walkthrough_pgn(pgn_obj, delay=1.0) -> None:
    """
    Allows one to walkthrough pgn game in jupyter notebooks.
    Saves SVG object in temporary file and displays on notebooks
    interface

    Args:
        pgn_obj (chess.png.game)
        delay(float): time between moves for display to update
    """

    pgn_io = StringIO(str(pgn_obj))
    game = chess.pgn.read_game(pgn_io)
    board = game.board()
    move_count = 1

    with TemporaryDirectory() as temp:
        for move in game.mainline_moves():
            mover = "White" if move_count % 2 == 0 else "Black"

            board.push(move)
            render_svg_board(board, temp,
                             f"Move {move_count}_{mover} to move.SVG")

            move_count += 1
            time.sleep(delay)
