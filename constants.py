""" Repository for constants used across library """
CONVENTIONAL_PIECE_VALUES = {'P': 1.,
                             'N': 3.,
                             'B': 3.,
                             'R': 5.,
                             'Q': 9.,
                             'K': 999.}

# python-chess is 1 indexed, so pad names with None @ 0 index
PIECE_NAMES = [None, "P", "N", "B", "R", "Q", "K"]
