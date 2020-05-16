""" Tools to simulate chess games """
from collections import Counter
import matplotlib.pyplot as plt
from tqdm import tqdm
import chess
import chess.pgn
import chess.svg


class ChessPlayground():
    """
    Class for experimenting with different engines & algorithms. This class
    handles the analysis of the various engines, including plotting data

    Attributes:
        white_engine (ChessEngine): engine for determining white moves
        black_engine (ChessEngine): engine for determining black moves
        game (chess.pgn.Game): game object
        board (chess.board): board representation
        terminal_conditions (Dict[function]): in form "name of terminal
            condition": "boolean method to test for condition"
        all_results (List[str]): containing strings describing all game
            results
        all_move_counts (List[int]): contains count of number of moves in
            each game played
        all_value_differentials (List[tuple]): contains mapping of value
            differential for each move across each game played in form
            (white engine evaluation, black engine evaluation) at each move

    Methods:
        play_game() -> None: plays a single game
        play_multiple_games(N) -> None: plays N games
        evaluate_ending_board() -> str: evaluates final board state to
            determine why game over
        display_all_results() -> None: plots bar chart of all game results
            played in instance
        display_value_differences(game_index) -> None: plot line chart of game
            values as evaluated by both engines
        display_all_results() -> None: plots all value differences for all
            games played
    """

    def __init__(self, white_engine, black_engine) -> None:
        """
        Setup empty game with defined engines for both sides
        Engines should evaluate board state and return a uci move

        Args:
            white_engine (ChessEngine)
            black_engine (ChessEngine)
        """

        self.white_engine = white_engine
        self.black_engine = black_engine

        self.game, self.board, self.terminal_conditions = None, None, None
        (self.all_results, self.all_move_counts,
            self.all_value_differentials) = ([], [], [])

    def play_game(self) -> None:
        """ Plays single game """
        # Initialize new game, reset value_differential count for each game
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
        self.all_value_differentials.append(
            tuple(zip(self.white_engine.value_differentials,
                      self.black_engine.value_differentials)))

        result = self.evaluate_ending_board()
        self.all_results.append(result)

    def play_multiple_games(self, N: int = 100) -> None:
        """
        Plays through N games, storing results in all_results
        Note: results values in all_results

        Args:
            N (int): number of games to play. Default=100
        """
        self.all_results = []
        progress_bar = tqdm(range(1, N+1))
        for game_number in progress_bar:
            progress_bar.set_description(f"Playing game {game_number}")
            self.play_game()

    def evaluate_ending_board(self) -> str:
        """
        Determines conditions leading to end of game

        Returns:
            (str): designating condition of game ending
        """
        result = self.board.result()

        if not self.board.is_game_over():
            return "Game not over"

        if result == "1-0":
            return "White win"

        if result == "0-1":
            return "Black win"

        # A different design pattern may be to move this var to the init
        # so as to not keep initializing it on each call, but I want to
        # explicitly initialize it on each call since it's dependent on
        # the current board state
        self.terminal_conditions = {
            'Checkmate': self.board.is_checkmate,
            'Stalemate': self.board.is_stalemate,
            'Insufficient material': self.board.is_insufficient_material,
            'Seventyfive moves': self.board.is_seventyfive_moves,
            'Fivefold repetition': self.board.is_fivefold_repetition}

        for title, condition in self.terminal_conditions.items():
            if condition():
                return title

        # If none of the defined ending states found, game ended due to
        # some variable endstate that would require further probing.
        # This would be the case if playing some variation
        return "Undetermined"

    def display_all_results(self):
        """
        Wrapper for matplotlib to display results of all games

        Returns:
            (collections.Counter): containing counts of all ending types
        """
        counts = Counter(self.all_results)

        _, ax = plt.subplots()
        ax.bar(counts.keys(), counts.values(),
               color='black', width=0.75, align='center')
        ax.set_xlabel('Terminal conditions')
        ax.set_ylabel('Number games')
        ax.set_title('Terminal conditions')

        return counts

    def display_value_differences(self, game_index) -> None:
        """
        Wrapper for matplotlib to plot difference in piece total
        values throughout game

        Args:
            game_index (int): index of game played in iteration of simulation
                to plot
        """
        game_values = self.all_value_differentials[game_index]
        white_engine_vals = [v[0] for v in game_values]
        black_engine_vals = [-v[1] for v in game_values]
        positive_mask = [True if e > 0 else False for e in white_engine_vals]

        _, axes = plt.subplots(2, 1, sharex=True)
        x = range(len(white_engine_vals))
        for idx, engine in enumerate([white_engine_vals, black_engine_vals]):
            axes[idx].fill_between(x, 0, engine, where=positive_mask,
                                   facecolor='floralwhite', interpolate=True)
            axes[idx].fill_between(x, 0, engine, where=[
                not x for x in positive_mask],
                facecolor='black', interpolate=True)
            axes[idx].plot(x, engine, color='black', linewidth=0.75)
            axes[idx].axhline(y=0, color='black', linewidth=0.5)

            if idx == 0:
                axes[idx].set_ylabel(
                    f"{self.white_engine.name} (white) evaluation")
            else:
                axes[idx].set_ylabel(
                    f"{self.black_engine.name} (black) evaluation")
                axes[idx].set_xlabel('Move index')

    def display_all_game_values(self) -> None:
        """ Wrapper for display_value_differences to plot results of
        all games """
        for game in range(len(self.all_value_differentials)):
            self.display_value_differences(game)
