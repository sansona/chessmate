""" Utility functions """
import time
from contextlib import contextmanager
from io import StringIO
from pathlib import Path
from collections import Counter
from tempfile import TemporaryDirectory
from typing import Union, List
import matplotlib.pyplot as plt  # type: ignore

import chess
import chess.pgn
import pytest  # type: ignore
from IPython.display import SVG, clear_output, display  # type: ignore

from constants import FEN_MAPS


@contextmanager
def not_raises(exception):
    """
    Opposite of pytest raises for when everything works fine
    https://stackoverflow.com/questions/20274987/how-to-use-pytest-to-check-that-error-is-not-raised
    """
    try:
        yield
    except exception:
        raise pytest.fail(f"DID RAISE {exception}")


def is_valid_fen(fen: str) -> bool:
    """
    Parses FEN string to see if format is valid

    Args:
        fen (str): fen notation of board

    Raises:
        TypeError: if type(fen) not str
        ValueError: if fen is string but isn't in FEN format

    Returns:
        (bool): True if valid
    """
    if not isinstance(fen, str):
        raise TypeError(f"Invalid FEN object type {type(fen)}")

    rows = fen.split("/")
    if len(rows) != 8:
        raise ValueError(f"Expected 8 rows in FEN position: {fen}")

    return True


def get_piece_at(
    board: chess.Board, position: Union[str, chess.Square]
) -> str:
    """
    Gets chess symbol of piece at position on board

    Args:
        board (chess.Board): current board state in python-chess object
        position (str/chess.Square): position of square i.e chess.A1 or "A1"

    Raises:
        AttributeError: if no piece on board at position

    Returns:
        (str): symbol of piece at square if any
    """
    # Convert position to chess.Square
    if isinstance(position, str):
        file, rank = ord(position[0].lower()) - 97, int(position[1]) - 1
        square = chess.square(file, rank)
    elif isinstance(position, chess.Square):
        square = position

    piece = board.piece_at(square)

    if piece:
        return piece.symbol()
    return ""


def display_pgn_text(pgn_obj: chess.pgn.Game) -> None:
    """
    Displays game loaded from pgn in text form

    Args:
        pgn_obj (chess.pgn.Game)
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


def render_svg_board(
    board: chess.Board, temp_dir: Union[str, Path], display_str: str
) -> None:
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
    fpath = Path(temp_dir) / f"{display_str}"
    with open(fpath, "w") as f:
        f.write(boardsvg)
    display(SVG(str(fpath)))
    print(fpath.stem)
    clear_output(wait=True)


def walkthrough_pgn(
    pgn_obj: chess.pgn.Game,
    fen: str = FEN_MAPS["standard"],
    delay: float = 1.0,
) -> None:
    """
    Allows one to walkthrough pgn game in jupyter notebooks.
    Saves SVG object in temporary file and displays on notebooks
    interface

    Args:
        pgn_obj (chess.pgn.Game)
        fen (str): fen notation of board. Default to standard
        delay(float): time between moves for display to update
    """
    pgn_io = StringIO(str(pgn_obj))
    game = chess.pgn.read_game(pgn_io)
    board = chess.Board(fen=fen)
    game.setup(board=board)
    move_count = 1

    with TemporaryDirectory() as temp:
        for move in game.mainline_moves():
            mover = "White" if move_count % 2 == 0 else "Black"

            board.push(move)
            render_svg_board(
                board, temp, f"Move {move_count}_{mover} to move.SVG"
            )

            move_count += 1
            time.sleep(delay)


def display_all_results(all_results: List[str]) -> Counter:
    """
    Wrapper for matplotlib to display results of all games in bar chart

    Args:
        all_results (List[str]): containing strings describing all game
            results
    Returns:
        (collections.Counter): containing counts of all ending types
    """
    counts = Counter(all_results)

    _, ax = plt.subplots()
    ax.bar(
        counts.keys(),
        counts.values(),
        color="black",
        width=0.75,
        align="center",
    )
    ax.set_xlabel("Terminal conditions")
    ax.set_ylabel("Number games")
    ax.set_title("Terminal conditions")

    return counts


def display_material_difference(
    material_differences: List[tuple], game_index: int
) -> None:
    """
    Wrapper for matplotlib to plot difference in piece total
    values throughout game

    Args:
        material_differences (List[tuple]): contains mapping of value
            differential for each move across each game played in form
            (white engine evaluation, black engine evaluation) at each move
        game_index (int): index of game played in iteration of simulation
            to plot
    """
    game_values = material_differences[game_index]
    engine_vals = [v[0] for v in game_values]
    positive_mask = [True if e > 0 else False for e in engine_vals]

    _, ax = plt.subplots(1, 1)
    x = range(len(engine_vals))
    ax.set_title(f"Game: {game_index}")
    ax.fill_between(
        x,
        0,
        engine_vals,
        where=positive_mask,
        facecolor="floralwhite",
        interpolate=True,
    )
    ax.fill_between(
        x,
        0,
        engine_vals,
        where=[not x for x in positive_mask],
        facecolor="black",
        interpolate=True,
    )
    ax.plot(x, engine_vals, color="black", linewidth=0.75)
    ax.axhline(y=0, color="black", linewidth=0.5)
    ax.set_ylabel("Material difference")
    ax.set_xlabel("Move index")


def display_all_material_differences(
    material_differences: List[tuple],
) -> None:
    """
    Wrapper for display_material_difference to plot results of
    all games

    Args:
        material_differences (List[tuple]): contains mapping of value
            differential for each move across each game played in form
            (white engine evaluation, black engine evaluation) at each move
    """
    for game_idx in range(len(material_differences)):
        display_material_difference(material_differences, game_idx)


def display_piece_value_table(piece_value_table):
    """
    Makes visual display of piece value table

    Args:
        piece_value_table ([List[Lists]])
    """
    pass
