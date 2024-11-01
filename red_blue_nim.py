import sys
import math
import random  

class RedBlueNim:
    def __init__(self, RM, BM, version="standard"):
        self.RM = RM  # Red marbles
        self.BM = BM  # Blue marbles
        self.CP = 0   # 0 for human, 1 for computer (current player)
        self.version = version  # Game version, "standard" or "misere"

    def is_game_over(self):
        return self.RM == 0 or self.BM == 0

    def GWS(self):  # Get winner based on game version and last player
        if self.is_game_over():
            if self.version == "standard":
                return "Computer" if self.CP == 0 else "Human"
            elif self.version == "misere":
                return "Human" if self.CP == 0 else "Computer"
        return None

    def GM(self):  # Generate moves
        moves = [(0, 2), (1, 2), (0, 1), (1, 1)]
        valid_moves = []
        for color, count in moves:
            if color == 0 and count <= self.RM:
                valid_moves.append((color, count))
            elif color == 1 and count <= self.BM:
                valid_moves.append((color, count))
        valid_moves.sort(key=lambda x: (self.RM if x[0] == 0 else self.BM))
        return valid_moves

    def MM(self, move):  # Make move
        color, count = move
        if color == 0:
            self.RM -= count
        else:
            self.BM -= count
        self.CP = 1 - self.CP  # Switch player

    def UM(self, move):  # Undo move
        color, count = move
        if color == 0:
            self.RM += count
        else:
            self.BM += count
        self.CP = 1 - self.CP  # Switch player back

    def evaluate(self):
        if self.is_game_over():
            # Winning or losing state
            return 1000 if self.GWS() == "Computer" else -1000
        smaller_pile_bonus = 5 if self.RM < self.BM else (-5 if self.BM < self.RM else 0)
        return (2 * self.RM + 3 * self.BM + smaller_pile_bonus) * (1 if self.CP == 1 else -1)

def minimax(game, depth, alpha, beta, maximizing_player):
    if game.is_game_over() or (depth == 0 if depth is not None else False):
        return game.evaluate(), None

    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        for move in game.GM():
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
        for move in game.GM():
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

import random  # Add this import at the top if not already present

def play_red_blue_nim(RM, BM, version="standard", FP="computer", depth=None):
    game = RedBlueNim(RM, BM, version)
    initial_marbles = RM + BM  # Track initial total marbles
    game.CP = 0 if FP == "human" else 1

    while not game.is_game_over():
        print(f"\nCurrent state: Red: {game.RM}, Blue: {game.BM}")

        if game.CP == 0:  # Human's turn
            valid_move = False
            while not valid_move:
                print("Your turn:")
                color_choice = input("Which color to remove (red or blue)? ").strip().lower()

                if color_choice == "red":
                    color = 0
                elif color_choice == "blue":
                    color = 1
                else:
                    print("Invalid color! Choose 'red' or 'blue'.")
                    continue

                try:
                    count = int(input("Remove how many marbles (1 or 2)? "))
                    move = (color, count)

                    if move in game.GM():
                        valid_move = True
                        game.MM(move)
                    else:
                        print("Invalid move! Try again.")
                except ValueError:
                    print("Please enter a valid number (1 or 2).")

        else:  # Computer's turn
            if depth == 0:
                available_moves = game.GM()
                winning_move = None
                for move in available_moves:
                    game.MM(move)
                    if game.is_game_over() and game.GWS() == "Computer":
                        winning_move = move
                    game.UM(move)
                    if winning_move:
                        break  # Stop if a winning move is found

                best_move = winning_move if winning_move else random.choice(available_moves)
            else:
                _, best_move = minimax(game, depth, -math.inf, math.inf, True)

            if best_move:
                game.MM(best_move)
                color_str = "red" if best_move[0] == 0 else "blue"
                print(f"Computer removed {best_move[1]} {color_str} marbles.")
            else:
                print("No valid moves for the computer.")
                break  # Exit if no valid moves for the computer

        if game.is_game_over():
            winner = game.GWS()
            if winner:
                remaining_marbles = game.RM + game.BM
                points = initial_marbles - remaining_marbles
                print(f"\n{winner} wins by {points} points!")
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
