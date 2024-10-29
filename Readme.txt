Name -  Patel TakshKumar Girishbhai
UTA ID - 1002248623.
Language Used - Python 3.10.9

Code Structure : 
1. state_evaluation(red, blue, is_misere): Calculate the score of the current state based on the quantity of marbles in the red and blue piles.
2. next_move(red, blue, pile, count): Update the number of marbles in the piles after a move is made.
3. generate_move(red, blue): Generate all feasible moves in the given state.
4. comp_move(red, blue, is_misere, depth): Use Minimax to determine the optimal move for the computer player.
5. minimax(red, blue, is_misere, depth, is_maximizing): Recursive function to determine the optimal move using Minimax.
6. main(): The main function to run the game.

How to run the code : 
1. Run the file red_blue_nim.py present in the zip folder.
2. Input the required data in the format given in the question. 
For eg. Run this script in the terminal - python red_blue_nim.py 5 6 standard human 2 (where red marbles are 5, blue marbles are 6, version is standard, first player will be human and depth taken is 2)
3. The game will start with the first player as human and you'll have to play the game till any one of the marbles(blue or red) count gets zero.
4. The end result will be generated, stating who won the game(human or computer) and their corresponding score.