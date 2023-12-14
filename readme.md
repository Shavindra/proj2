# README.md for Argumentation Framework Programs

## Overview

This repository contains two Python programs developed for exploring different aspects of Argumentation Frameworks (AFs) as part of a Knowledge Representation project. The programs are:

1. **preferred_game.py** - Implements a Socratic discussion-based game within an AF.
2. **semantics.py** - Focuses on the semantics of AFs, particularly on credulous acceptance under selected semantics.

## 1. Preferred Game (`preferred_game.py`)

### Description
`preferred_game.py` is based on Socratic discussion principles and operates within a loaded argumentation framework. The game initiates with the proponent's argument, following which the user (opponent) can respond with counter-arguments. The interaction continues until one party wins. The program follows specific game rules and winning criteria as outlined in the assignment.

### Usage
To run the game:
```bash
python preferred_game.py <path_to_json_file> <claimed_argument>

# python preferred_game.py ./graphs/graph2.json 1
```

- `<path_to_json_file>`: The path to the JSON file containing the argumentation framework.
- `<claimed_argument>`: The initial argument of the proponent.

### Rules and Winning Conditions
1. The opponent can only attack arguments made by the proponent in the current or previous rounds.
2. The proponent must counter-attack the opponent's latest argument.
3. The opponent cannot repeat arguments, but the proponent can.
4. Winning conditions are based on argument repetition, inability to move, and exhaustion of choices.

## 2. Semantics Analysis (semantics.py)
### Description
semantics.py implements the evaluation of arguments under chosen semantics. It calculates preferred extensions to assess if a given argument is credulously accepted under these semantics. This program emphasizes the practical application of theoretical concepts, particularly in evaluating and accepting arguments within an AF.

### Usage
To evaluate an argument:

```bash
python semantics.py <path_to_af_file> <argument>

# python semantics.py ./graphs/graph2.json 1  
```

- `<path_to_af_file>`: The file path to the AF.
- `<argument>`: The argument to be evaluated for credulous acceptance.

### Functionality
1. Calculates the largest or maximal complete extensions (preferred extensions).
2. Checks if the given argument is included in any preferred extensions.
3. Outputs whether the argument is credulously acceptable under the selected semantics.

