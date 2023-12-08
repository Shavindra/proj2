import sys
import json

class ArgumentationFramework:
    def __init__(self, arguments, attack_relations):
        # arguments: dict of argument numbers to argument strings
        self.arguments = arguments
        # attack_relations: list of tuples of the form (attacker, attacked)
        self.attack_relations = attack_relations
        # attacks: dict of argument numbers to list of arguments that it attacks
        self.attacks = {arg: [] for arg in arguments}
        # Populate the attacks dict
        for attacker, attacked in attack_relations:
            # attacker attacks attacked
            self.attacks[attacker].append(attacked)


class DiscussionGame:
    def __init__(self, framework, claimed_argument):
        self.framework = framework
        self.claimed_argument = claimed_argument
        self.current_argument = claimed_argument
        self.proponent_arguments = set([claimed_argument])  # Start with the claimed argument
        self.opponent_arguments = set()
        self.round = 0

    def proponent_move(self):
        if self.round > 0:
            # Select valid moves that attack the last argument chosen by the opponent
            potential_moves = [move for move, attacked in self.framework.attack_relations if attacked == self.current_argument]
            valid_moves = [move for move in potential_moves if move not in self.opponent_arguments]

            if valid_moves:
                self.current_argument = valid_moves[0]
            else:
                return "opponent"

            self.proponent_arguments.add(self.current_argument)
        self.round += 1
        return self.current_argument

    def opponent_move(self, argument):
        # Check if the argument is a valid move
        if argument not in self.framework.arguments:
            return "invalid"  # Argument does not exist

        # Check if the argument attacks any of the proponent's arguments
        if not any(arg in self.proponent_arguments for arg in self.framework.attacks[argument]):
            return "invalid"  # Argument does not attack any of the proponent's arguments

        # Add the argument to the set of opponent's arguments
        self.opponent_arguments.add(argument)
        self.current_argument = argument

        return "valid"

    def check_win_condition(self):
        # Removed condition where opponent wins if the current argument is in their arguments
        if not self.framework.attacks[self.current_argument] or all(arg in self.opponent_arguments for arg in self.framework.attacks[self.current_argument]):
            return "opponent"
        elif not any(arg in self.framework.attacks[self.current_argument] and arg not in self.opponent_arguments for arg in self.framework.arguments):
            return "proponent"
        return "continue"

def play_game(game):
    print("Welcome to the Preferred Discussion Game!")
    print("You are the opponent. Try to attack the argument presented by the proponent.\n")

    while True:
        proponent_move = game.proponent_move()
        if proponent_move == "opponent":
            print("You win! The proponent cannot make a move.")
            break

        print(f"Round {game.round}: Proponent's argument: '{game.framework.arguments[proponent_move]}'")

        # Find arguments that attack the current argument
        possible_moves = [attacker for attacker, attacked in game.framework.attack_relations if attacked == proponent_move]
        print("Possible moves for you:")
        for move in possible_moves:
            print(f"  {move}: {game.framework.arguments[move]}")

        if not possible_moves:
            print("Proponent wins! No more moves left for the opponent.")
            break

        opponent_move = input("Your move (enter argument number): ")
        if game.opponent_move(opponent_move) == "invalid":
            print("Invalid move. Try again.")
            continue

        # Check win condition after opponent's move and proponent's subsequent move
        if game.check_win_condition() == "opponent":
            print("You win!")
            break

        print("\nNext round...\n")


# Load JSON data from a file and start the game with the given argument
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_json_file> <claimed_argument>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    claimed_argument = sys.argv[2]

    try:
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)

        framework = ArgumentationFramework(json_data["Arguments"], json_data["Attack Relations"])
        game = DiscussionGame(framework, claimed_argument)
        play_game(game)
    except Exception as e:
        print(f"Error: {e}")
