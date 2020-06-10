""" Repository for FEN constants.used across library """

# maps commonly used FENs to unique strs
pawns = "pppppppp"
standard = "rnbqkbnr"
river = "8/8/8/8"
suffix = " w KQkq - 0 1"
central_rows = f"/{pawns}/{river}/{pawns.upper()}/"

# Setup FEN for different combinations.
knights_no_bishops = "rnnqknnr"
bishops_no_knights = "rbbqkbbr"
rooks_no_queens = "rnbrkbnr"
queens_no_rooks = "qnbqkbnq"
mayhem = "qqqqkqqq"

FEN_MAPS = {
    "standard": (f"{standard}{central_rows}{standard.upper()}{suffix}"),
    "minor_knights_only": (
        f"{knights_no_bishops}{central_rows}"
        f"{knights_no_bishops.upper()}{suffix}"
    ),
    "minor_bishops_only": (
        f"{bishops_no_knights}{central_rows}"
        f"{bishops_no_knights.upper()}{suffix}"
    ),
    "rooks_no_queens": (
        f"{rooks_no_queens}{central_rows}" f"{rooks_no_queens.upper()}{suffix}"
    ),
    "queens_no_rooks": (
        f"{queens_no_rooks}{central_rows}" f"{queens_no_rooks.upper()}{suffix}"
    ),
    "white_standard_black_knights": (
        f"{knights_no_bishops}{central_rows}" f"{standard.upper()}{suffix}"
    ),
    "white_knights_black_standard": (
        f"{standard}{central_rows}" f"{knights_no_bishops.upper()}{suffix}"
    ),
    "white_standard_black_bishops": (
        f"{bishops_no_knights}{central_rows}" f"{standard.upper()}{suffix}"
    ),
    "white_bishops_black_standard": (
        f"{standard}{central_rows}" f"{bishops_no_knights.upper()}{suffix}"
    ),
    "white_mayhem": (f"{standard}{central_rows}{mayhem.upper()}{suffix}"),
    "black_mayhem": (f"{mayhem}{central_rows}{standard.upper()}{suffix}"),
    "mayhem": (f"{mayhem}{central_rows}{mayhem.upper()}{suffix}"),
    "pandemonium": (
        f"{mayhem}/{mayhem}/{river}/"
        f"{mayhem.upper()}/{mayhem.upper()}{suffix}"
    ),
    "easy_white_win": "8/5k2/1P2q3/3n4/3B4/6Q1/4K3/1R6 w - - 0 1",
    "easy_black_win": "6r1/4k3/2q3n1/8/8/3Q1N2/4K3/8 w - - 0 1",
}
