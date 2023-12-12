import sys
import json

class ArgumentationFramework:
    def __init__(self, arguments, attack_relations):
        self.arguments = arguments
        self.attack_relations = attack_relations
        self.attacks = {arg: [] for arg in arguments}
        for attacker, attacked in attack_relations:
            self.attacks[attacker].append(attacked)

class DiscussionGame:
    def __init__(self, framework, claimed_argument):
        self.framework = framework
        self.claimed_argument = claimed_argument
        self.current_argument = claimed_argument
        self.proponent_arguments = set([claimed_argument])
        self.opponent_arguments = set()
        self.round = 0

    def proponent_move(self):
        if self.round > 0:
            potential_moves = [move for move, attacked in self.framework.attack_relations if attacked == self.current_argument]
            valid_moves = [move for move in potential_moves if move not in self.opponent_arguments]
            non_admissable_moves = [move for move, attacked in self.framework.attack_relations if attacked in self.proponent_arguments]
            self_conflicting_moves = [move for move, attacked in self.framework.attack_relations if attacked == move]
            prefered_valid_moves = [move for move in valid_moves if ((move not in self_conflicting_moves)and(move not in non_admissable_moves))]

            
            if prefered_valid_moves:
                self.current_argument = prefered_valid_moves[0]
            elif valid_moves:
                self.current_argument = valid_moves[0]
            else:
                return "opponent"
            self.proponent_arguments.add(self.current_argument)
        self.round += 1
        return self.current_argument

    def opponent_move(self, argument):
        if argument not in self.framework.arguments:
            return "invalid"

        # Ensure the argument attacks the current proponent's argument
        if argument not in [attacker for attacker, attacked in self.framework.attack_relations if attacked == self.current_argument]:
            return "invalid"

        self.opponent_arguments.add(argument)
        self.current_argument = argument
        return "valid"

    def check_win_condition(self):
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

        print(f"Round {game.round}: Proponent's argument: {proponent_move}: '{game.framework.arguments[proponent_move]}'")

        valid_moves = [attacker for attacker, attacked in game.framework.attack_relations if attacked == proponent_move and attacker not in game.opponent_arguments]

        print("Possible moves for you:")
        for move in valid_moves:
            print(f"  {move}: {game.framework.arguments[move]}")

        if not valid_moves:
            print("Proponent wins! No more moves left for the opponent.")
            break

        while True:
            opponent_move = input("Your move (enter argument number): ")
            move_result = game.opponent_move(opponent_move)
            if move_result == "invalid":
                print("Invalid move. Try again.")
                continue
            break

        if game.check_win_condition() == "opponent":
            print("You win!")
            break

        print("\nNext round...\n")

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
