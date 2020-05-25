# chessmate
> chessmate is a python package that enables analyses and defining of chess engines

## Usage example

### Engines
The basic building block of chessmate is the engine. All engines inherit
from ```chess.engines.BaseEngine``` and obey an evaluate-move progression wherein the engine evaluates the current board
state by some metric and/or algorithm and returns a single move it deems best.

Examples of some simple engines are:
  1. ```Random``` - returns a random move
  2. ```PrioritizePawnMoves``` - prioritizes all moves pawn related 
  3. ```CaptureHighestValue``` - prioritize capturing the highest value piece available
  4. ```ScholarsMate``` - obeys standard Scholar's Mate sequence and resigns if unsuccessful
  
Since most chess engines can be boiled down to this basic progression, the chessmate engine schema provides a simple but
powerful framework for developing and analyzing engines

---
### Game simulations
Once engines are defined, one can perform analysis via the classes available in ```chess.simulations```. Some example functionality includes:

Simulating a game between two engines:

``` 
from chessmate.simulations import ChessPlayground
from chessmate.engines import CaptureHighestValue, Random

# Setup simulated game between ScholarsMate engine on white and CaptureHighestValue engine on black.
simulation = ChessPlayground(ScholarsMate(), CaptureHighestValue())
simulation.play_game()
```

Simulating multiple games
```
# Setups multiple independently simulated games
simulation.play_multiple_games(1000)
```

You can also play directly against an engine in the IPython console:
```
playvs = PlayVsEngine(CaptureHighestValue())
playvs.play_game()
```

---
### Basic analysis

To evaluate the results of a simulation:

Since the ```ScholarsMate``` engine either successfully mates or resigns, we'd expect a small percentage of games to be won by white mating and the rest black by resignation.
```
from chessmate.analysis import display_all_results
display_all_results(simulation.all_results)
```
![results](https://user-images.githubusercontent.com/17757035/82768134-f3b2b880-9de1-11ea-9b96-8a3be118fb80.png)

To view the difference in material across a game or games
```
from chessmate.analysis import display_material_difference

# Use CaptureHighestvalue on white and Random engine on black
simulation = ChessPlayground(CaptureHighestValue(), Random())
simulation.play_multiple_games(10)
display_material_difference(simulation.game_pgns, game_index=0)
display_material_difference(simulation.game_pgns, game_index=4)
```
![game_0](https://user-images.githubusercontent.com/17757035/82768042-21e3c880-9de1-11ea-98a9-6c7804a37113.png)
![game 4](https://user-images.githubusercontent.com/17757035/82768041-214b3200-9de1-11ea-83b7-9439652ac777.png)

To visualize the events of a game, chessmate comes with IPython functionality to display games in the console move by move
```
from chess.utils import walkthrough_pgn
walkthrough_pgn(simulation.game_pgns[0])
```
![display](https://user-images.githubusercontent.com/17757035/82768462-07f7b500-9de4-11ea-83ec-97975e9e9017.png)

---
## Meta
Jiaming Chen –  jiaming.justin.chen@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/sansona/chessmate](https://github.com/sansona/)
