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
            return 3 * self.blue_marbles
        elif self.blue_marbles == 0:
            return 2 * self.red_marbles
        else:
            return None

    def generate_moves(self, version):
        if version == "standard":
            moves = [(2, 0), (0, 2), (1, 0), (0, 1)]
        else:
            moves = [(0, 1), (1, 0), (0, 2), (2, 0)]
        valid_moves = []
        for move in moves:
            if (move[0] > 0 and move[0] <= self.red_marbles) or (move[1] > 0 and move[1] <= self.blue_marbles):
                valid_moves.append(move)
        return valid_moves

    def make_move(self, move):
        red_remove, blue_remove = move
        self.red_marbles -= red_remove
        self.blue_marbles -= blue_remove
        self.current_player = 1 - self.current_player  # Switch player

    def undo_move(self, move):
        # Undo the move by adding back the marbles removed
        red_add, blue_add = move
        self.red_marbles += red_add
        self.blue_marbles += blue_add
        self.current_player = 1 - self.current_player  # Switch player back

    def evaluate(self):
        return 2 * self.red_marbles + 3 * self.blue_marbles

def minimax(game, depth, alpha, beta, maximizing_player):
    if game.is_game_over() or depth == 0:
        return game.evaluate(), None

    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        for move in game.generate_moves("standard"):
            game.make_move(move)
            eval, _ = minimax(game, depth - 1, alpha, beta, False)
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
            eval, _ = minimax(game, depth - 1, alpha, beta, True)
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
        if game.current_player == current_player:
            if current_player == 0:
                print(f"\nCurrent state: Red: {game.red_marbles}, Blue: {game.blue_marbles}")
                valid_move = False
                while not valid_move:
                    print("Your turn:")
                    red_remove = int(input("Remove how many red marbles (1 or 2)? "))
                    blue_remove = int(input("Remove how many blue marbles (1 or 2)? "))
                    if (red_remove, blue_remove) in game.generate_moves(version):
                        valid_move = True
                    else:
                        print("Invalid move! Try again.")
                game.make_move((red_remove, blue_remove))
            else:
                _, best_move = minimax(game, depth, -math.inf, math.inf, True)
                game.make_move(best_move)
                print(f"Computer removed {best_move[0]} red marbles and {best_move[1]} blue marbles.")
        else:
            _, best_move = minimax(game, depth, -math.inf, math.inf, True)
            game.make_move(best_move)

    winner_score = game.get_winner_score()
    if winner_score is None:
        print("It's a draw!")
    elif winner_score > 0:
        print("You win!")
    else:
        print("Computer wins!")

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
