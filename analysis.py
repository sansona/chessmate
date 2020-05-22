""" Functions for analyzing board states and results of games """
from typing import List
from collections import Counter
import matplotlib.pyplot as plt
import chess
from constants import CONVENTIONAL_PIECE_VALUES, PIECE_NAMES


def tabulate_board_values(board: chess.Board) -> float:
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
        'Checkmate': board.is_checkmate,
        'Stalemate': board.is_stalemate,
        'Insufficient material': board.is_insufficient_material,
        'Seventyfive moves': board.is_seventyfive_moves,
        'Fivefold repetition': board.is_fivefold_repetition}

    for title, condition in terminal_conditions.items():
        if condition():
            return title

    # If none of the defined ending states found, game ended due to
    # some variable endstate that would require further probing.
    # This would be the case if playing some variation
    return "Undetermined"


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
    ax.bar(counts.keys(), counts.values(),
           color='black', width=0.75, align='center')
    ax.set_xlabel('Terminal conditions')
    ax.set_ylabel('Number games')
    ax.set_title('Terminal conditions')

    return counts


def display_material_difference(material_differences: List[tuple],
                                game_index: int) -> None:
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
    white_engine_vals = [v[0] for v in game_values]
    black_engine_vals = [-v[1] for v in game_values]
    positive_mask = [True if e > 0 else False for e in white_engine_vals]

    _, axes = plt.subplots(2, 1, sharex=True)
    x = range(len(white_engine_vals))
    for idx, engine in enumerate([white_engine_vals, black_engine_vals]):
        axes[idx].set_title(f"Game: {game_index}")
        axes[idx].fill_between(x, 0, engine, where=positive_mask,
                               facecolor='floralwhite', interpolate=True)
        axes[idx].fill_between(x, 0, engine, where=[
            not x for x in positive_mask],
            facecolor='black', interpolate=True)
        axes[idx].plot(x, engine, color='black', linewidth=0.75)
        axes[idx].axhline(y=0, color='black', linewidth=0.5)

        if idx == 0:
            axes[idx].set_ylabel("White evaluation")
        else:
            axes[idx].set_ylabel("Black evaluation")
            axes[idx].set_xlabel('Move index')


def display_all_material_differences(material_differences: List[tuple]) -> None:
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
