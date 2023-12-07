import json

def load_argumentation_framework(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_valid_attacks(current_argument, attack_relations):
    return [target for source, target in attack_relations if source == current_argument]

def game_loop(arguments, attack_relations, start_argument):
    current_argument = start_argument
    used_arguments = {current_argument}
    turn = 0  # 0 for proponent, 1 for opponent

    while True:
        if turn == 0:  # Computer's turn
            print(f"Computer's argument: {arguments[current_argument]}")
            valid_attacks = get_valid_attacks(current_argument, attack_relations)
            if not valid_attacks:
                print("Opponent wins! Proponent cannot make a move.")
                break
            current_argument = valid_attacks[0]  # Simplified logic for computer's move
        else:  # User's turn
            print(f"Current argument: {arguments[current_argument]}")
            valid_attacks = get_valid_attacks(current_argument, attack_relations)
            valid_attacks = [arg for arg in valid_attacks if arg not in used_arguments]

            if not valid_attacks:
                print("Proponent wins! Opponent has no valid moves left.")
                break

            print("Choose an argument to attack with:")
            for i, arg in enumerate(valid_attacks):
                print(f"{i}: {arguments[arg]}")

            choice = int(input("Your choice (number): "))
            current_argument = valid_attacks[choice]
            used_arguments.add(current_argument)

        if current_argument in used_arguments and turn == 0:
            print("Opponent wins! Proponent repeats an argument.")
            break

        turn = 1 - turn  # Switch turns

def main():
    file_path = input("Enter the file path of the argumentation framework: ")
    framework = load_argumentation_framework(file_path)

    print("Available Arguments:")
    for arg_id, arg_text in framework['Arguments'].items():
        print(f"{arg_id}: {arg_text}")

    start_argument = input("Choose the starting argument (ID): ")
    if start_argument not in framework['Arguments']:
        print("Invalid argument ID.")
        return

    game_loop(framework['Arguments'], framework['Attack Relations'], start_argument)

if __name__ == "__main__":
    main()
