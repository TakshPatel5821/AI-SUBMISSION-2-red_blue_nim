import sys
import math

class RedBlueNim:
    def __init__(self, RM, BM):
        self.RM = RM #BLUE MARBLE
        self.BM = BM # RED MARBLE
        self.CP = 0  # 0 for human, 1 for computer (CUREENT PLAYER)
        self.HC = None   # Track the color selected by the human

    def is_game_over(self):
        return self.RM == 0 or self.BM == 0

    def GWS(self):   #THIS IS FOR WINNER SCORE
        if self.RM == 0:
            return -3 * self.BM  # Human loses; scoring reflects their loss
        elif self.BM == 0:
            return 2 * self.RM  # Computer wins; scoring reflects its gain
        else:
            return None

    def GM(self, version): #GENERATE MOVES
        if version == "standard":
            moves = [(0, 2), (1, 2), (0, 1), (1, 1)]  # Order for standard version
        else:
            moves = [(1, 1), (0, 1), (1, 2), (0, 2)]  # Inverted order for misère version

        valid_moves = []
        for color, count in moves:
            if color == 0 and count <= self.RM:
                valid_moves.append((color, count))
            elif color == 1 and count <= self.BM:
                valid_moves.append((color, count))
        return valid_moves

    def MM(self, move):    #THIS IS FOR MAKE MOVE
        color, count = move
        if color == 0:
            self.RM -= count
        else:
            self.BM -= count
        self.CP = 1 - self.CP  # Switch player

    def UM(self, move):   #UNDO MOVE
        color, count = move
        if color == 0:
            self.RM += count
        else:
            self.BM += count
        self.CP = 1 - self.CP  # Switch player back

    def evaluate(self):
        return 2 * self.RM + 3 * self.BM

def minimax(game, depth, alpha, beta, maximizing_player):
    if game.is_game_over() or (depth == 0 if depth is not None else False):
        return game.evaluate(), None

    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        for move in game.GM("standard"):
            game.MM(move)
            eval, _ = minimax(game, (depth - 1) if depth is not None else None, alpha, beta, False)
            game.UM(move)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = None
        for move in game.GM("misere"):
            game.MM(move)
            eval, _ = minimax(game, (depth - 1) if depth is not None else None, alpha, beta, True)
            game.UM(move)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def play_red_blue_nim(RM, BM, version="standard", FP="computer", depth=None):
    game = RedBlueNim(RM, BM)

    # Set the first player
    game.CP = 0 if FP == "human" else 1

    while not game.is_game_over():
        print(f"\nCurrent state: Red: {game.RM}, Blue: {game.BM}")

        if game.CP == 0:  # Human's turn
            valid_move = False
            while not valid_move:
                print("Your turn:")
                color_choice = input("Which color to remove (red or blue)? ").strip().lower()

                # Determine human's color choice
                if color_choice == "red":
                    color = 0
                    game.HC = "red"  # Human is playing red
                elif color_choice == "blue":
                    color = 1
                    game.HC = "blue"  # Human is playing blue
                else:
                    print("Invalid color! Choose 'red' or 'blue'.")
                    continue

                try:
                    count = int(input("Remove how many marbles (1 or 2)? "))
                    move = (color, count)

                    if move in game.GM(version):
                        valid_move = True
                        game.MM(move)
                    else:
                        print("Invalid move! Try again.")
                except ValueError:
                    print("Please enter a valid number (1 or 2).")

        else:  # Computer's turn
            color = 1 if game.HC == "red" else 0  # Computer plays the opposite color
            _, best_move = minimax(game, depth, -math.inf, math.inf, True)
            if best_move:
                game.MM(best_move)
                color_str = "red" if best_move[0] == 0 else "blue"
                print(f"Computer removed {best_move[1]} {color_str} marbles.")
            else:
                print("No valid moves for the computer.")
                break  # Exit if no valid moves for the computer

        # Check if the game is over and display the winner if so
        if game.is_game_over():
            winner_score = game.GWS()
            if winner_score is not None:
                if winner_score > 0:
                    print(f"\nYou win by {winner_score} points!")
                else:
                    print(f"\nComputer wins by {-winner_score} points!")
            else:
                print("\nIt's a draw!")
            break  # Exit loop when the game is over

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: red_blue_nim.py <num-red> <num-blue> [<version>] [<first-player>] [<depth>]")
        sys.exit(1)

    RM = int(sys.argv[1])
    BM = int(sys.argv[2])
    version = sys.argv[3] if len(sys.argv) >= 4 else "standard"
    FP = sys.argv[4].lower() if len(sys.argv) >= 5 else "computer"
    depth = int(sys.argv[5]) if len(sys.argv) >= 6 else None

    if FP not in {"computer", "human"}:
        print("Invalid first player. Choose 'computer' or 'human'.")
        sys.exit(1)

    play_red_blue_nim(RM, BM, version, FP, depth)
