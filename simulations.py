""" Tools to simulate chess games """
from tempfile import TemporaryDirectory
from tqdm import tqdm
import chess
import chess.pgn
import chess.svg
from analysis import evaluate_ending_board
from utils import render_svg_board


class PlayVsEngine():
    """
    Class for playing against engine move by move in jupyter notebook

    Attributes:
        engine (engines.BaseEngine): engine to play against
        game (chess.pgn.Game): game object
        board (chess.board): board representation
        node (chess.Board.node): gametree object for storing moves

    Methods:
        player_move() -> None: allows player to push UCI move
        engine_move() -> None: allows engine to evaluate boardstate and push
            a move
        play_game(play_as) -> None: wrapper around player_move() & engine_move()
            with built-in logic to allow move by move play
        display_board() -> None: generic function to display board. Wrapper
            around utils.render_svg_board()
    """

    def __init__(self, engine):
        """ Setups empty board and engine """
        self.engine = engine
        self.game = chess.pgn.Game()
        self.board = self.game.board()
        self.node = None

    def player_move(self) -> None:
        """ Allows player to push UCI move with current boardstate """
        legal_move = False
        while not legal_move:
            # Stay in loop until player enters a legal move - catches
            # non-UCI inputs & illegal moves
            try:
                move_input = chess.Move.from_uci(str(input()))
            except ValueError:
                self.display_board(f"Move not recognized - {str(move_input)}")
                continue

            if move_input in self.board.legal_moves:
                legal_move = True
                self.board.push_uci(str(move_input))
            else:
                self.display_board(f"Not legal move - {str(move_input)}")

        # Store data in gametree node
        if self.board.fullmove_number == 1:
            self.node = self.game.add_variation(move_input)
        else:
            self.node = self.node.add_variation(move_input)

        self.display_board(
            f"Move {self.board.fullmove_number} - engine to move.")

    def engine_move(self) -> None:
        """ Allows engine to evaluate board and push UCI move """
        eng_move = self.engine.move(self.board)
        self.board.push_uci(str(eng_move))

        if self.board.fullmove_number == 1:
            self.node = self.game.add_variation(eng_move)
        else:
            self.node = self.node.add_variation(eng_move)

        self.display_board(
            f"Move {self.board.fullmove_number}- player to move.")

    def play_game(self, play_as='white') -> None:
        """
        Wrapper around player_move() & engine_move() with simple logic built in
        to determine move order

        Args:
            play_as (str): side to play game as. Default='white'
        """
        self.display_board(
            f"Move {self.board.fullmove_number} - ready for first move.")

        while not self.board.is_game_over():
            if play_as == 'white':
                self.player_move()
                # Include checks after every move whether game over since
                # python chess only checks for game over at beginning of move
                # pair i.e on white's turn
                if self.board.is_game_over():
                    break
                self.engine_move()
            else:
                self.engine_move()
                if self.board.is_game_over():
                    break
                self.player_move()

        self.display_board(f"{evaluate_ending_board(self.board)}!")

    def display_board(self, display_str) -> None:
        """
        Wrapper around utils.render_svg_board with temporary directory
        context manager

        Args:
            display_str (str): str to display beneath board for board state
                context
        """
        with TemporaryDirectory() as temp:
            render_svg_board(self.board, temp, display_str)


class ChessPlayground():
    """
    Class for experimenting with different engines & algorithms. This class
    handles the analysis of the various engines, including plotting data

    Attributes:
        white_engine(ChessEngine): engine for determining white moves
        black_engine(ChessEngine): engine for determining black moves
        game(chess.pgn.Game): game object
        board(chess.board): board representation
        terminal_conditions(Dict[function]): in form "name of terminal
            condition": "boolean method to test for condition"
        game_pgns(List(chess.pgn.Game.node)): list of all pgn data for
            games played
        all_results(List[str]): containing strings describing all game
            results
        all_move_counts(List[int]): contains count of number of moves in
            each game played
        all_material_differences(List[tuple]): contains mapping of value
            differential for each move across each game played in form
            (white engine evaluation, black engine evaluation) at each move

    Methods:
        play_game() -> None: plays a single game
        play_multiple_games(N) -> None: plays N games
    """

    def __init__(self, white_engine, black_engine) -> None:
        """
        Setup empty game with defined engines for both sides
        Engines should evaluate board state and return a uci move

        Args:
            white_engine(ChessEngine)
            black_engine(ChessEngine)
        """

        self.white_engine = white_engine
        self.black_engine = black_engine

        self.game, self.board, self.terminal_conditions = None, None, None
        (self.game_pgns, self.all_results, self.all_move_counts,
            self.all_material_differences) = [], [], [], []

    def play_game(self) -> None:
        """ Plays single game """
        self.game = chess.pgn.Game()
        self.board = self.game.board()
        self.white_engine.reset_game_variables()
        self.black_engine.reset_game_variables()

        while not self.board.is_game_over():
            # If white ends game on move, don't execute black move
            white_move = self.white_engine.move(self.board)
            self.board.push_uci(str(white_move))
            if self.board.fullmove_number == 1:
                # on first move, setup game tree
                node = self.game.add_variation(white_move)
            else:
                node = node.add_variation(white_move)

            # If white's move doesn't end game, play black's move
            if not self.board.is_game_over():
                black_move = self.black_engine.move(self.board)
                self.board.push_uci(str(black_move))
                node = node.add_variation(black_move)

        # At end of game, store number of moves in game, value of pieces on
        # board throughout game, and reason for ending game
        self.all_move_counts.append(self.board.fullmove_number - 1)
        self.all_material_differences.append(
            tuple(zip(self.white_engine.material_difference,
                      self.black_engine.material_difference)))

        self.game_pgns.append(self.game)
        self.all_results.append(evaluate_ending_board(self.board))

    def play_multiple_games(self, N: int = 100) -> None:
        """
        Plays through N games, storing results in all_results
        Note: results values in all_results

        Args:
            N(int): number of games to play. Default = 100
        """
        self.all_results = []
        progress_bar = tqdm(range(1, N+1))
        for game_number in progress_bar:
            progress_bar.set_description(f"Playing game {game_number}")
            self.play_game()
