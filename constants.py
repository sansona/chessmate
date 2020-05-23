""" Repository for constants used across library """

# Since python-chess doesn't provide functionality for getting piece
# at square via. string notation, setup own board to map strings to
# squares
from typing import Dict


def make_board_repr() -> Dict[str, float]:
    """
    Make representation of board

    Returns:
        Dict[str, float]
    """
    SQUARE_STR = []
    for letter in 'ABCDEFGH':
        file = [f"{letter}{r}" for r in reversed(range(1, 9,))]
        SQUARE_STR.extend(file)
    return SQUARE_STR


CONVENTIONAL_PIECE_VALUES = {'P': 1.,
                             'N': 3.,
                             'B': 3.,
                             'R': 5.,
                             'Q': 9.,
                             'K': 999.}

# python-chess is 1 indexed, so pad names with None @ 0 index
PIECE_NAMES = [None, "P", "N", "B", "R", "Q", "K"]

# python-chess maps colors to bool, so unmap them here for better
# user interfacing
COLOR_MAP = {True: 'White', False: 'Black'}

# maps commonly used FENs to unique strs
pawns = 'pppppppp'
standard = 'rnbqkbnr'
river = '8/8/8/8'
suffix = ' w KQkq - 0 1'
central_rows = f"/{pawns}/{river}/{pawns.upper()}/"

# Setup FEN for different combinations.
knights_no_bishops = 'rnnqknnr'
bishops_no_knights = 'rbbqkbbr'
rooks_no_queens = 'rnbrkbnr'
queens_no_rooks = 'qnbqkbnq'
mayhem = 'qqqqkqqq'

FEN_MAPS = {
    'standard': (f'{standard}{central_rows}{standard.upper()}{suffix}'),
    'minor_knights_only': (f'{knights_no_bishops}{central_rows}'
                           f'{knights_no_bishops.upper()}{suffix}'),
    'minor_bishops_only': (f'{bishops_no_knights}{central_rows}'
                           f'{bishops_no_knights.upper()}{suffix}'),
    'rooks_no_queens': (f'{rooks_no_queens}{central_rows}'
                        f'{rooks_no_queens.upper()}{suffix}'),
    'queens_no_rooks': (f'{queens_no_rooks}{central_rows}'
                        f'{queens_no_rooks.upper()}{suffix}'),
    'white_standard_black_knights': (f'{knights_no_bishops}{central_rows}'
                                     f'{standard.upper()}{suffix}'),
    'white_knights_black_standard': (f'{standard}{central_rows}'
                                     f'{knights_no_bishops.upper()}{suffix}'),
    'white_standard_black_bishops': (f'{bishops_no_knights}{central_rows}'
                                     f'{standard.upper()}{suffix}'),
    'white_bishops_black_standard': (f'{standard}{central_rows}'
                                     f'{bishops_no_knights.upper()}{suffix}'),
    'white_mayhem': (f'{standard}{central_rows}{mayhem.upper()}{suffix}'),
    'black_mayhem': (f'{mayhem}{central_rows}{standard.upper()}{suffix}'),
    'mayhem': (f'{mayhem}{central_rows}{mayhem.upper()}{suffix}'),
    'pandemonium': (f'{mayhem}/{mayhem}/{river}/'
                    f'{mayhem.upper()}/{mayhem.upper()}{suffix}')}
