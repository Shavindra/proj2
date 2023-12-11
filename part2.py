import json
import sys
from itertools import combinations

class ArgumentationFramework:
    """
    Represents an argumentation framework with arguments and attack relations.
    """
    def __init__(self, arguments, attack_relations):
        self.arguments = arguments
        self.attack_relations = attack_relations

    def is_conflict_free(self, args):
        """
        Checks if a set of arguments is conflict-free.
        """
        for attack in self.attack_relations:
            if (attack[0] in args and attack[1] in args) or (attack[0] == attack[1] and attack[0] in args):
                return False
        print(f"Set {args} is conflict-free.")
        return True
        
    def characteristic_function(self, S):
        """
        Computes the characteristic function for a set S of arguments.
        """
        result = set()
        for a in self.arguments.keys():
            attacked = False
            for attack in self.attack_relations:
                if attack[1] == a and attack[0] in S:
                    attacked = True
                    break
            if not attacked:
                result.add(a)
        print(f"Characteristic function for set {S} is {result}.")
        return result

    def is_defended(self, argument, args):
        """
        Checks if an argument is defended by a given set of arguments.
        An argument is defended if for every attack on it, there is a counter-attack from the set.
        """
        for attack in self.attack_relations:
            if attack[1] == argument:
                defended = False
                for counter_attack in self.attack_relations:
                    if counter_attack[0] in args and counter_attack[1] == attack[0]:
                        defended = True
                        break
                if not defended:
                    return False
        return True

    def admissible_sets(self):
        """
        Determines admissible sets of arguments.
        """
        admissible = []
        for r in range(len(self.arguments) + 1):
            for subset in combinations(self.arguments, r):
                subset_set = set(subset)
                if self.is_conflict_free(subset_set) and all(self.is_defended(arg, subset_set) for arg in subset_set):
                    admissible.append(subset_set)
        print(f"Admissible sets are {admissible}.")
        return admissible

    def complete_extensions(self):
        """
        Computes complete extensions of the framework.
        """
        admissible = self.admissible_sets()
        complete = []

        for admissible_set in admissible:
            defended_arguments = {arg for arg in self.arguments if self.is_defended(arg, admissible_set)}
            if admissible_set == defended_arguments:
                complete.append(admissible_set)

        print(f"Complete extensions are {complete}.")
        return complete

    def preferred_extensions(self):
        """
        Computes preferred extensions of the framework.
        Preferred extensions are the largest (maximal) complete extensions.
        """
        complete_exts = self.complete_extensions()
        
        max_length = max(len(ext) for ext in complete_exts) if complete_exts else 0
        preferred_exts = [ext for ext in complete_exts if len(ext) == max_length]
        print(f"Preferred extensions are {preferred_exts}.")
        return preferred_exts

    def credulous_acceptance(self, claimed_argument):
        """
        Checks if an argument is credulously accepted under preferred semantics.
        """
        preferred_exts = self.preferred_extensions()
        for ext in preferred_exts:
            if claimed_argument in ext:
                return True
        return False

def play_game(framework, claimed_argument):
    """
    Plays the discussion game for a given argument in the framework.
    """
    if framework.credulous_acceptance(claimed_argument):
        print(f"Argument {claimed_argument} is credulously accepted under preferred semantics.")
    else:
        print(f"Argument {claimed_argument} is not credulously accepted under preferred semantics.")

def validate_argument(argument, valid_arguments):
    """
    Validates if the given argument is within the range of valid arguments.
    """
    return argument in valid_arguments

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_json_file> <claimed_argument>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    claimed_argument = sys.argv[2]

    try:
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)

        if not validate_argument(claimed_argument, json_data["Arguments"].keys()):
            print(f"Invalid argument. Please enter a valid argument number from: {list(json_data['Arguments'].keys())}")
            sys.exit(1)

        framework = ArgumentationFramework(json_data["Arguments"], json_data["Attack Relations"])
        play_game(framework, claimed_argument)
    except Exception as e:
        print(f"Error: {e}")
