""" Repository for constants used across library """

# Since python-chess doesn't provide functionality for getting piece
# at square via. string notation, setup own board to map strings to
# squares
SQUARE_STR = []
for letter in 'ABCDEFGH':
    file = [f"{letter}{r}" for r in range(1, 9)]
    SQUARE_STR.extend(file)

CONVENTIONAL_PIECE_VALUES = {'P': 1.,
                             'N': 3.,
                             'B': 3.,
                             'R': 5.,
                             'Q': 9.,
                             'K': 999.}

# python-chess is 1 indexed, so pad names with None @ 0 index
PIECE_NAMES = [None, "P", "N", "B", "R", "Q", "K"]
