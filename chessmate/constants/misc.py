""" Repository for misc/general constants.used across chessmate """
# python-chess is 1 indexed, so pad names with None @ 0 index
PIECE_NAMES = [None, "P", "N", "B", "R", "Q", "K"]

# python-chess maps colors to bool, so unmap them here for better
# user interfacing
COLOR_MAP = {True: "White", False: "Black"}

# Indexing used for hashes
PIECE_INDEXING = {
    "P": 0,
    "p": 1,
    "N": 2,
    "n": 3,
    "B": 4,
    "b": 5,
    "R": 6,
    "r": 7,
    "Q": 8,
    "q": 9,
    "K": 10,
    "k": 11,
}
