""" Repository for misc/general constants used across chessmate """
# python-chess is 1 indexed, so pad names with None @ 0 index
PIECE_NAMES = [None, "P", "N", "B", "R", "Q", "K"]

# python-chess maps colors to bool, so unmap them here for better
# user interfacing
COLOR_MAP = {True: "White", False: "Black"}
