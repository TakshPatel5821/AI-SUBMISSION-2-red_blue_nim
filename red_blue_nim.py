import sys
import math

class RedBlueNim:
    def __init__(self, red_marbles, blue_marbles):
        self.red_marbles = red_marbles
        self.blue_marbles = blue_marbles
        self.current_player = 0  # 0 for human, 1 for computer

    def is_game_over(self):
        return self.red_marbles == 0 or self.blue_marbles == 0

    def get_winner_score(self):
        if self.red_marbles == 0:
            return 3 * self.blue_marbles  # Computer wins if red marbles are 0
        elif self.blue_marbles == 0:
            return 2 * self.red_marbles  # Human wins if blue marbles are 0
        else:
            return None

    def generate_moves(self, version):
        moves = [(0, 1), (0, 2), (1, 1), (1, 2)]
        valid_moves = []
        for color, count in moves:
            if color == 0 and count <= self.red_marbles:
                valid_moves.append((color, count))
            elif color == 1 and count <= self.blue_marbles:
                valid_moves.append((color, count))
        return valid_moves

    def make_move(self, move):
        color, count = move
        if color == 0:
            self.red_marbles -= count
        else:
            self.blue_marbles -= count
        self.current_player = 1 - self.current_player  # Switch player

    def undo_move(self, move):
        color, count = move
        if color == 0:
            self.red_marbles += count
        else:
            self.blue_marbles += count
        self.current_player = 1 - self.current_player  # Switch player back

    def evaluate(self):
        return 2 * self.red_marbles + 3 * self.blue_marbles

def minimax(game, depth, alpha, beta, maximizing_player):
    if game.is_game_over() or (depth == 0 if depth is not None else False):
        return game.evaluate(), None

    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        for move in game.generate_moves("standard"):
            game.make_move(move)
            eval, _ = minimax(game, (depth - 1) if depth is not None else None, alpha, beta, False)
            game.undo_move(move)
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
        for move in game.generate_moves("misere"):
            game.make_move(move)
            eval, _ = minimax(game, (depth - 1) if depth is not None else None, alpha, beta, True)
            game.undo_move(move)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def play_red_blue_nim(red_marbles, blue_marbles, version="standard", first_player="computer", depth=None):
    game = RedBlueNim(red_marbles, blue_marbles)
    current_player = 1 if first_player == "computer" else 0

    while not game.is_game_over():
        print(f"\nCurrent state: Red: {game.red_marbles}, Blue: {game.blue_marbles}")

        if game.current_player == 0:  # Human's turn
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
                    if move in game.generate_moves(version):
                        valid_move = True
                        game.make_move(move)
                    else:
                        print("Invalid move! Try again.")
                except ValueError:
                    print("Please enter a valid number (1 or 2).")
        else:  # Computer's turn
            _, best_move = minimax(game, depth, -math.inf, math.inf, True)
            if best_move:
                game.make_move(best_move)
                color_str = "red" if best_move[0] == 0 else "blue"
                print(f"Computer removed {best_move[1]} {color_str} marbles.")
            else:
                print("No valid moves for the computer.")
                break  # Exit if no valid moves for the computer

        # Check if the game is over and display the winner if so
        if game.is_game_over():
            winner_score = game.get_winner_score()
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

    red_marbles = int(sys.argv[1])
    blue_marbles = int(sys.argv[2])
    version = sys.argv[3] if len(sys.argv) >= 4 else "standard"
    first_player = sys.argv[4].lower() if len(sys.argv) >= 5 else "computer"
    depth = int(sys.argv[5]) if len(sys.argv) >= 6 else None

    if first_player not in {"computer", "human"}:
        print("Invalid first player. Choose 'computer' or 'human'.")
        sys.exit(1)

    play_red_blue_nim(red_marbles, blue_marbles, version, first_player, depth)
