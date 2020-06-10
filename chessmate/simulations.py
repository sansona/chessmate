""" Tools to simulate chess games """
from tempfile import TemporaryDirectory
from typing import Callable, Dict, List, Union

import chess  # type: ignore
import chess.pgn  # type: ignore
import chess.svg  # type: ignore
from tqdm import tqdm  # type: ignore

from chessmate.analysis import evaluate_ending_board
from chessmate.constants.fens import FEN_MAPS
from chessmate.constants.misc import COLOR_MAP
from chessmate.utils import is_valid_fen, render_svg_board


class EnginePlay:
    """
    Base class for engine play. Used in classes in which engines
    have to interact with a game state

    Attributes:
        game (chess.pgn.Game(): pgn game representation
        board (chess.Board): board object with fen functionality
        fen (str): FEN representation of board setup
        node (chess.pgn.GameNode): gametree object for storing moves

    Methods:
        play_game (): general function to play a standalone game
        append_move_to_tree (chess.Move): appends move to game tree
            representation. Used to store game state
    """

    def __init__(self):
        self.game: chess.pgn.Game = chess.pgn.Game()
        self._fen: str = FEN_MAPS["standard"]
        self._board: chess.Board = chess.Board(fen=self._fen)
        self.node: chess.pgn.GameNode = None

    @property
    def board(self) -> chess.Board:
        """ Getter for board """
        return self._board

    @board.setter
    def board(self, fen_str: str) -> None:
        """
        Setter for setting board with new fen

        Args:
            fen_str (str): fen representation of board
        Raise:
            ValueError: if FEN is invalid given board setup
        """
        if is_valid_fen(fen_str):
            try:
                self._board = chess.Board(fen=fen_str)
            except ValueError:
                print(f"Invalid FEN: {fen_str}")

    @property
    def fen(self) -> str:
        """ Getter for fen """
        return self._fen

    @fen.setter
    def fen(self, fen_str: str) -> None:
        """
        Setter for setting new fen. Updates self.board with new fen

        Args:
            fen_str (str): fen representation of board
        Raise:
            ValueError: if FEN is invalid given board setup
        """
        if is_valid_fen(fen_str):
            try:
                self._fen = fen_str
                self._board = chess.Board(fen=fen_str)
            except ValueError:
                print(f"Invalid FEN: {fen_str}")

    def play_game(self) -> None:
        """ Main function for wrapping around game play functionality """
        raise NotImplementedError("Function move not implemented")

    def append_move_to_tree(self, move: chess.Move) -> None:
        """
        Appends move to gametree representation

        Args:
            move (chess.Move): move in UCI object
        """
        if self._board.fullmove_number == 1:
            # If first move, initiate root node
            self.node = self.game.add_variation(move)
        else:
            self.node = self.node.add_variation(move)


class PlayVsEngine(EnginePlay):
    """
    Class for playing against engine move by move in jupyter notebook

    Attributes:
        engine (engines.BaseEngine): engine to play against
        board (chess.board): board representation
        player_side (chess.Color/bool): chess.WHITE or chess.BLACK for
            side to play as. Note that since python-chess encodes the color
            as a bool, decode it as color for displaying

    Methods:
        player_move() -> chess.Move: allows player to push UCI move
        engine_move() -> chess.Move: allows engine to evaluate boardstate and
            push a move. Null if engine resigns
        play_game() -> None: wrapper around player_move() & engine_move()
            with built-in logic to allow move by move play
        display_board() -> None: function to display board. Wrapper around
            utils.render_svg_board()
    """

    def __init__(self, engine):
        """ Setups empty board and engine """
        super().__init__()
        self.engine = engine
        self._board: chess.Board = chess.Board()
        self._player_side: Union[chess.Color, bool] = chess.WHITE

    def __repr__(self):
        """ Print out current state of playvsengine. Useful for
        printing out machinations of PlayVsEngine"""
        return f"""engine: {self.engine}
                player_side: {self._player_side}
                FEN: {self._board.fen}"""

    @property
    def player_side(self) -> str:
        """ Defining getter for player_side. Since chess.Color encoded as
        bool, remap to color string for user intepretation """
        return COLOR_MAP[self._player_side]

    @player_side.setter
    def player_side(self, side: Union[chess.Color, bool]) -> None:
        """ Setter function for player_side - chess.Color/bool inputs valid """
        if not isinstance(side, bool):
            raise TypeError(
                f"Invalid self.player_side ({self._player_side}) "
                "not in (chess.WHITE, chess.BLACK)"
            )
        self._player_side = side

    def player_move(self) -> chess.Move:
        """
        Allows player to push UCI move with current boardstate

        Returns
            (chess.Move): UCI object of move input
        """
        legal_move = False
        while not legal_move:
            # Stay in loop until player enters a legal move - catches
            # non-UCI inputs & illegal moves
            input_str = str(input())
            if input_str in ("res", "resign", "quit"):
                return chess.Move.null()

            # Catch non-UCI moves
            try:
                input_move = chess.Move.from_uci(input_str)
            except ValueError:
                self.display_board(f"Move not recognized - {str(input_move)}")
                continue

            if input_move in self._board.legal_moves:
                legal_move = True
                self._board.push_uci(str(input_move))
            else:
                # Catch non-legal moves
                self.display_board(f"Not legal move - {str(input_move)}")

        self.append_move_to_tree(input_move)
        self.display_board(
            f"Move {self._board.fullmove_number} - engine to move."
        )

        return input_move

    def engine_move(self) -> chess.Move:
        """
        Allows engine to evaluate board and push UCI move

        Returns:
            (chess.Move): UCI move from engine evaluation. Null if engine
                resigned
        """
        eng_move = self.engine.move(self._board)
        self._board.push_uci(str(eng_move))
        self.append_move_to_tree(eng_move)
        self.display_board(
            f"Move {self._board.fullmove_number} - player to move."
        )

        return eng_move

    def play_game(self) -> None:
        """
        Wrapper around player_move() & engine_move() with simple logic built in
        to determine move order

        Raises:
            TypeError: on initializing invalid self._player_side type
        """
        self.display_board(
            f"Move {self._board.fullmove_number} - ready for first move."
        )

        # Break out of loop by checking after each move is game over. For each
        # move, check if move results in game over or if move is null. Null
        # represents resignation
        while not self._board.is_game_over():
            if self._player_side == chess.WHITE:
                user_move = self.player_move()
                if user_move == chess.Move.null():
                    break
                if self._board.is_game_over():
                    break

                # python-chess doesn't have a resign option, so if engine
                # returns null move, take as resignation and end game
                eng_move = self.engine_move()
                if eng_move == chess.Move.null():
                    break
            if self._player_side == chess.BLACK:
                eng_move = self.engine_move()
                if eng_move == chess.Move.null():
                    break
                if self._board.is_game_over():
                    break
                user_move = self.player_move()
                if user_move == chess.Move.null():
                    break

        self.display_board(f"{evaluate_ending_board(self._board)}!")

    def display_board(self, display_str: str) -> None:
        """
        Wrapper around utils.render_svg_board with temporary directory
        context manager.

        Args:
            display_str (str): str to display beneath board for board state
                context
        """
        with TemporaryDirectory() as temp:
            render_svg_board(self._board, temp, display_str)


class ChessPlayground(EnginePlay):
    """
    Class for experimenting with different engines & algorithms. This class
    handles the analysis of the various engines, including plotting data

    Attributes:
        white_engine (ChessEngine): engine for determining white moves
        black_engine (ChessEngine): engine for determining black moves
        terminal_conditions (Dict[function]): in form "name of terminal
            condition": "boolean method to test for condition"
        game_pgns (List[chess.pgn.Game]): list for storage of all pgn data for
            games played
        all_results (List[str]): storage containing strings describing all game
            results
        all_move_counts (List[int]): storage for count of number of move
            in each game played
        all_material_differences (List[tuple]): contains mapping of value
            differential for each move across each game played in form
            (white engine evaluation, black engine evaluation) at each move

    Methods:
        play_game() -> None: plays a single game
        play_multiple_games(N) -> None: plays N games. Wrapper around
            play_game()
    """

    def __init__(self, white_engine, black_engine):
        """
        Setup empty game with defined engines for both sides

        Args:
            white_engine (ChessEngine)
            black_engine (ChessEngine)
        """
        super().__init__()
        self.white_engine = white_engine
        self.black_engine = black_engine
        self.terminal_conditions: Dict[str, Callable] = None
        self.game_pgns: List[chess.pgn.Game] = []
        self.all_results: List[str] = []
        self.all_move_counts: List[int] = []
        self.all_material_differences: List[tuple] = []

    def __repr__(self):
        """ Print out current state of playground """
        return f"""white engine: {self.white_engine}
                black engine: {self.black_engine}
                all_results: {self.all_results}
                all_move_counts: {self.all_move_counts}"""

    def play_game(self) -> None:
        """ Plays single game """
        self.game = chess.pgn.Game()
        self.game.setup(self._fen)
        # All game variables have to be reset from game to game. By default
        # reset() resets the board to starting fen, so set _board to
        # starting board to ensure set fen carries over
        starting_board = chess.Board(self._fen)
        self._board.reset()
        self._board = starting_board
        self.white_engine.reset_game_variables()
        self.black_engine.reset_game_variables()

        while not self._board.is_game_over():
            # If white ends game on move, don't execute black move
            white_move = self.white_engine.move(self._board)
            if white_move == chess.Move.null():
                break

            self._board.push_uci(str(white_move))
            self.append_move_to_tree(white_move)

            # If white's move doesn't end game, play black's move
            if not self._board.is_game_over():
                black_move = self.black_engine.move(self._board)
                if black_move == chess.Move.null():
                    break
                self._board.push_uci(str(black_move))
                self.append_move_to_tree(black_move)

        # At end of game, store number of moves in game, value of pieces on
        # board throughout game, and reason for ending game
        self.all_move_counts.append(self._board.fullmove_number - 1)
        self.all_material_differences.append(
            tuple(
                zip(
                    self.white_engine.material_difference,
                    self.black_engine.material_difference,
                )
            )
        )

        self.game_pgns.append(self.game)
        self.all_results.append(evaluate_ending_board(self._board))

    def play_multiple_games(self, N: int = 100) -> None:
        """
        Plays through N games, storing results in all_results
        Note: results values in all_results

        Args:
            N(int): number of games to play. Default = 100
        """
        self.all_results = []
        progress_bar = tqdm(range(1, N + 1))
        for game_number in progress_bar:
            progress_bar.set_description(f"Playing game {game_number}")
            self.play_game()
