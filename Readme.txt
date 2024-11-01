Name -  Patel TakshKumar Girishbhai
UTA ID - 1002248623.
Language Used - Python 3.10.9

Code Structure : 
1. Attributes:
            RM (int): Red marbles.
            BM (int): Blue marbles.
            CP (int): Current player (0 for human, 1 for computer).
            version (str): "standard" (last marble wins) or "misere" (last marble loses).
2. Methods:

            __init__: Initializes marbles, player, and version.
            is_game_over: Checks if any marble count is zero.
            get_winner: Determines winner based on version and last move.
            generate_moves: Lists valid moves as (color, count) tuples.
            make_move: Executes a move, updates marble count and player.
            undo_move: Reverses a move, restoring marble count and player.
            evaluate: Heuristic evaluation favoring human or computer.+
3. Function: minimax
            Uses Minimax with alpha-beta pruning to find the best move for the computer or human by evaluating possible game states.
4. Function: play_red_blue_nim
            Runs the game loop, prompting human input and selecting computer moves via Minimax or randomly if depth=0.

How to run the code : 
1. Run the file red_blue_nim.py present in the zip folder.
2. Input the required data in the format given in the question. 
For eg. Run this script in the terminal - python red_blue_nim.py 5 6 standard human 2 (where red marbles are 5, blue marbles are 6, version is standard, first player will be human and depth taken is 2)
3. The game will start with the first player as human and you'll have to play the game till any one of the marbles(blue or red) count gets zero.
4. The end result will be generated, stating who won the game(human or computer) and their corresponding score.