#!/usr/bin/env python3
from z3 import *
import random
import argparse
import os
import sys

"""
Car puzzle solver:
- Option 1: Generate a random puzzle
- Option 2: Load an existing manual puzzle from a .txt file in the same directory

Manual puzzle file format:
- Grid of N lines, each with N whitespace-separated tokens
- Tokens:
    X  = empty cell
    Z  = goal cell (rendered as [X] / [P] / [a] in output)
    P  = main car (horizontal, must be length 1, must start col 0)
    p  = main car (vertical, must be length 1, must start row 0)
    A,B,C,... = horizontal obstacle cars (uppercase)
    a,b,c,... = vertical obstacle cars (lowercase)

Example:
 X  B  B  X  X
 X  X  b  X  X
 P  X  b  X  Z
 X  X  X  X  X
 A  A  A  X  X
"""

# --------------------------------------------------------------------------------------------------
# 1) Random puzzle generation
# --------------------------------------------------------------------------------------------------

def generate_random_board(N, num_obstacles, main_orientation="H", max_car_len=None, seed=None):
    # A seed is a starting point for the pseudo-random generator. Giving the same seed makes the generator produce the same sequence of random values, which means the puzzle generator creates the same puzzle everytime. This is useful for debugging, so we can test a specific puzzle several times. If the seed is None, Python uses a time-based value, so we get a different puzzle every run.
    if seed is not None:
        random.seed(seed)

    # If the user didn't specify a maximum car length, allow obstacle cars up to length N. Although, in practice, we should use values like 2 or 3.
    if max_car_len is None:
        max_car_len = N

    # Choose the main car's starting point and the goal cell. Main car is always length 1.
    if main_orientation == "H": # If the main car is horizontal (H)
        rowP = random.randrange(N) # Pick a random row for P, and stays on that row
        start = (rowP, 0) # Starts on the left edge (first column)
        goal = (rowP, N - 1) # Reaches right edge (last column)
    else:  # If the main car is vertical (V)
        colP = random.randrange(N) # Pick a random column for P, and stays on that column
        start = (0, colP) # Starts on the top edge (first row)
        goal = (N - 1, colP) # Reaches bottom edge (last row)

    cars = [] # This starts as an empty list, but it will eventually contain all cars. Just ahead we will append the main car (first car) and it will be placed in the cars[0] position. And later we will append the randomly placed obstacle cars.
    occupied = set() # This is to track occupied cells in order to never place a new car on top of an existing one. We'll store coordinates as tuples (row, col). For example, {(4,0), (1,2),(2,2),(3,2)}. A set has no order btw.

    main_symbol = 'P' if main_orientation == "H" else 'p' # Define the symbol convention for the main car. P if horizontal, and p is vertical. This symbol is only for display for illustrative purposes.

    # Main car P dictionary (data structure)
    P = {
        "name": "P",
        "ori": main_orientation,
        "len": 1,
        "row0": start[0], # start is a tuple. start[0] is the first element, which corresponds to the row
        "col0": start[1], # start[1] is the second element, which corresponds to the column
        "symbol": main_symbol,
    }
    cars.append(P)
    occupied.add(start) # Add the starting cell of the main car to the occupied, so no obstacle can overlap

    def car_cells(ori, length, r, c): # Returns all the cells a car would occupy, given orientation (H or V), length and head position (r, c). Head = leftmost cell for horizontal cars, topmost cell for vertical cars
        if ori == "H":
            return [(r, c + k) for k in range(length)] # For horizontal cars, it extends to the right from the head
        else:
            return [(r + k, c) for k in range(length)] # For vertical cars, it extends downwards from the head

    attempts_limit = 2000 # To avoid infinite loops, we limit the number of attempts
    attempts = 0

    # These are the symbols for obstacle cars. "horiz_syms" is a list that already contains all the letters from A to Z, except P.
    horiz_syms = [chr(ord('A') + i) for i in range(26) if chr(ord('A') + i) != 'P'] # We start from i=0, which corresponds to 'A', and then i=1, which corresponds to 'B', and so on, until i=25, which corresponds to 'Z'. The letter 'P' is explicitly excluded because it is reserved for the main car
    vert_syms = [chr(ord('a') + i) for i in range(26)]

    # Track which symbol we should assign next for each orientation. First horizontal obstacle gets 'A', then 'B', .... These counters also let us detect if we run out of letters (too many cars for the alphabet)
    horiz_idx = 0
    vert_idx = 0

    while len(cars) < num_obstacles + 1 and attempts < attempts_limit: # Place obstacle cars, until the number of cars in the board is equal to the number of obstacle cars + the main car
        attempts += 1

        ori = random.choice(["H", "V"]) # Randomly choose the orientation of this new obstacle
        length = random.randint(1, max_car_len) # Randomly choose a length between 1 and max_car_len

        if ori == "H":
            r = random.randrange(N) # Place the car in any row from 0 till N (excluding N)
            c = random.randrange(N - length + 1) # Place the car in any column from 0 till the right edge, while allowing space for the length of the car to fit. So, from 0 till N - length + 1 (excluding)
        else:
            r = random.randrange(N - length + 1)
            c = random.randrange(N)

        # Computes all grid cells that the car would occupy. For example, if ori == "V", length == 3, and (r,c) == (1,2), then the car would occupy: {(1,2), (2,2), (3,2)}. We haven't placed the car yet, we are just checking overlaps.
        cells = car_cells(ori, length, r, c)

        # If any of the cells that this car would occupy are already being occupied by another car, then this placement is invalid, so we skip it and try again going back to the beginning of the while cycle
        if any(cell in occupied for cell in cells):
            continue

        if P["ori"] == "H" and ori == "H" and r == P["row0"]: # If the main car is horizontal, we must not place another horizontal car on the same row. P["row0"] stores the row where the main car starts. We must skip this car placement scenario
            continue
        if P["ori"] == "V" and ori == "V" and c == P["col0"]:
            continue

        if ori == "H":
            if horiz_idx >= len(horiz_syms): # If we are on the first try (horiz_idx = 0) and we haven't reached all the letters available in the list of possible letters (0 < len(horiz_syms)), then the symbol (sym) of this car should be horiz_syms[0] = 'A', and the next horiz_idx should be incremented 1 value, so horiz_idx = 1.
                continue
            sym = horiz_syms[horiz_idx]
            horiz_idx += 1
        else:
            if vert_idx >= len(vert_syms):
                continue
            sym = vert_syms[vert_idx]
            vert_idx += 1

        idx = len(cars) # This represents the number of cars placed on the board. The main car was added first, so the first obstacle will have idx = 1. We use this value to give each obstacle a unique internal name like "C1", "C2", ...
        car = {
            "name": f"C{idx}", # internal name used only by the solver, for example, C1, C2, ...
            "ori": ori,
            "len": length,
            "row0": r, # row of the head of the car
            "col0": c, # column of the head of the car
            "symbol": sym, # symbol we assigned to the car recently
        }
        cars.append(car) # Add the car to the list of all cars on the board
        for cell in cells:
            occupied.add(cell) # Add the cells this car occupies to the occupied list of tuples

    if len(cars) < num_obstacles + 1:
        raise RuntimeError(f"Could not place all obstacle cars after {attempts_limit} attempts")

    return cars, goal


# --------------------------------------------------------------------------------------------------
# 2) Manual puzzle reading/validation
# --------------------------------------------------------------------------------------------------

def read_grid_from_file(path):
    with open(path, "r") as f: # open and read the text file that contains the puzzle grid
        lines = [line.rstrip("\n") for line in f if line.strip()] # For each line in the file f, if after removing the spaces (" "), tabs ("\t") and newlines ("\n") at the beginning and the end of the string it's still not empty, then remove the trailing newline character "\n", if it's there.
        # f:
        # " X B B X X \n" -> "X B B X X" is not empty, so we remove "\n" at the end, and it becomes "X B B X X"
        # " X X b X X \n"
        # " P X b X Z \n"
        # " X X X X X \n"
        # " A A A X X \n"
        # " \n"           -> "" is empty, so the line is discarded
        #
        # lines = ["X B B X X","X X b X X","P X b X Z","X X X X X","A A A X X"]

    # Split each line by whitespace to get a 2D grid, for example: "X B B X X" -> ["X","B","B","X","X"]
    grid = [line.split() for line in lines]

    row_lengths = {len(row) for row in grid} # Creates a set of all row lengths. If all rows have the same length 5, then row_lengths = {5}. If the second row was length 4, then row_lengths = {4,5}, which means there is at least one row with 4 columns, and at least one row with 5 columns. len(row) is the number of columns in each row of the grid
    if len(row_lengths) != 1: # If there's at least one row with a different length
        raise ValueError(f"Board is not rectangular: row lengths = {row_lengths}")

    N = len(grid) # Gives the number of rows
    if next(iter(row_lengths)) != N: # Compares all the values in the row_lengths set with the number of rows N (to check if it's a square, we check if the number of columns of the rows is different to the number of rows)
        raise ValueError(f"Board is not square: got {N} rows, {next(iter(row_lengths))} columns")

    return grid


def validate_and_build_cars(grid):
    N = len(grid) # Number of rows of the grid

    for r in range(N):
        for c in range(N):
            ch = grid[r][c]
            if ch == 'X' or ch == 'Z':
                continue # If the ch is either 'X' or 'Z', we go back to the for cycle and check the next grid[r][c]
            if not ch.isalpha(): # .isalpha() means a letter (uppercase or lowercase)
                raise ValueError(f"Invalid character '{ch}' at ({r},{c})")

    goals = [(r, c) for r in range(N) for c in range(N) if grid[r][c] == 'Z'] # Stores all the cells that contain a goal, for example, one goal will be: goals = [(2, 4)]
    if len(goals) == 0:
        raise ValueError("No goal cell 'Z' found")
    if len(goals) > 1:
        raise ValueError(f"Multiple goal cells 'Z' found at {goals}")
    goal_r, goal_c = goals[0] # Extract goal_r = 2 and goal_c = 4 from goals[0] == (2, 4), for example

    positions = {} # positions is a dictionary that maps each car symbol to a list of grid coordinates where it appears
    for r in range(N):
        for c in range(N):
            ch = grid[r][c]
            if ch == 'X' or ch == 'Z':
                continue
            positions.setdefault(ch, []).append((r, c)) # If ch is not already a key in 'positions', create it with an empty list ([]), else, just return the existing list. Add the current cell's coordinates to that list.
            # For example, in:
            # X B B X X
            # X X b X X
            # P X b X Z
            # X X X X X
            # A A A X X

            # The dictionary is going to look like this: ('B' is the "key", and [(0, 1), (0, 2)] are the "values")
            # positions = {
            #  'B': [(0, 1), (0, 2)],
            #  'b': [(1, 2), (2, 2)],
            #  'P': [(2, 0)],
            #  'A': [(4, 0), (4, 1), (4, 2)]
            # }
    if not positions: # If no car positions were added to the 'positions' dictionary
        raise ValueError("No cars found on the board")

    main_symbols = [s for s in positions.keys() if s in ('P', 'p')] # Collect all keys that are 'P' or 'p' (main car)
    if len(main_symbols) == 0:
        raise ValueError("No main car 'P' or 'p' found")
    if len(main_symbols) > 1:
        raise ValueError(f"Multiple main car symbols {main_symbols} found")
    main_sym = main_symbols[0]

    cars = [] # This is a list to store all cars, including main car and obstacles cars. Each element of this list will be a dictionary describing one car. Later, positions will be stored as row[i][t], col[i][t] where 'i' is the car index.
    # For example:
    # {
    #    "name": "C1",
    #    "ori": "H",
    #    "len": 3,
    #    "row0": 0,
    #    "col0": 1,
    #    "symbol": "B"
    # }
    main_index = None # This should be the index of the main car, however, at this point, we still don't assign a value

    for sym, cells in positions.items(): # 'sym' is the "key" and 'cells' are the "values"
        # Example: For sym = 'B', we have cells = [(0,1), (0,2)]
        rows = {r for (r, _) in cells} # rows = {0} (all segments are in the same row)
        cols = {c for (_, c) in cells} # cols = {1,2}

        if len(cells) == 1: # If the symbol appears exactly once, it's a one cell car.
            (r0, c0) = cells[0]
            ori = "H" if sym.isupper() else "V" # Orientation defined by the convetion in the beginning of the code
            length = 1
        else: # If the symbol appears multiple times, we deduce orientation by checking if all segments share a row or column
            if len(rows) == 1: # Segments share a row, so it's a horizontal car
                ori = "H"
                r0 = next(iter(rows)) # 'rows' is a set, not a list, therefore, it cannot be indexed using r0 = rows[0]. We already know that len(rows) == 1 (exactly one row), so we extract the first value from the set
                sorted_cols = sorted(c for (_, c) in cells) # Extract the column index from each (row, col) tuple in 'cells' and sort them from left to right. Example: if cells happens to be [(0,2), (0,1)], this produces [1, 2]. Sorting ensures a consistent left-to-right order regardless of how the grid was read, allowing to check if the car's cells are consecutive next.
                for i in range(len(sorted_cols) - 1):
                    if sorted_cols[i + 1] != sorted_cols[i] + 1: # car's cells are not consecutive (there's a gap)
                        raise ValueError(f"Car '{sym}' is not contiguous horizontally")
                c0 = sorted_cols[0] # We treat the leftmost column as the car's head position
                length = len(cells)
            elif len(cols) == 1:
                ori = "V"
                c0 = next(iter(cols)) # Extract the first (and only) value from the "cols" set
                sorted_rows = sorted(r for (r, _) in cells) # Extract the row index from each tuple (row, col) in cells and sort them from top to bottom
                for i in range(len(sorted_rows) - 1):
                    if sorted_rows[i + 1] != sorted_rows[i] + 1: # car's cells are not consecutive (there's a gap)
                        raise ValueError(f"Car '{sym}' is not contiguous vertically")
                r0 = sorted_rows[0] # We treat the topmost row as the car's head position
                length = len(cells)
            else:
                raise ValueError(f"Car '{sym}' cells are neither in a single row nor a single column")

        if ori == "H" and sym.islower():
            raise ValueError(f"Car '{sym}' is lowercase but horizontal (expected vertical)")
        if ori == "V" and sym.isupper():
            raise ValueError(f"Car '{sym}' is uppercase but vertical (expected horizontal)")

        car = {
            "name": sym if sym not in ('P', 'p') else "P",
            "ori": ori,
            "len": length,
            "row0": r0, # head row (topmost for vertical, only row value for horizontal)
            "col0": c0, # head col (leftmost for horizontal, only col value for vertical)
            "symbol": sym,
        }
        if sym == main_sym: # If this symbol is the main car, remember its index in the 'cars' list. So, len(cars) is exactly the position it will occupy after cars.append(car) next
            main_index = len(cars)
            
        cars.append(car) # Add this car dictionary to the end of the list of cars
        # cars = [ # "cars" list
        #    {"name": "B", "ori": "H", "row0": 0, "col0": 1},
        #    {"name": "b", "ori": "V", "row0": 1, "col0": 2},
        #    {"name": "P", "ori": "H", "row0": 2, "col0": 0}, # main_index = 2
        #    {"name": "A", "ori": "H", "row0": 4, "col0": 0},
        # ]

    if main_index is None:
        raise ValueError("Internal error: could not locate main car index")

    main_car = cars[main_index] # Retrieve the main car dictionary using the index recorded earlier when we encountered the main symbol in the grid

    if main_car["len"] != 1: # Defensive programming, once again
        raise ValueError(f"Main car '{main_sym}' must have length 1, got {main_car['len']}")

    if main_car["ori"] == "H":
        if main_car["col0"] != 0: # the head of the horizontal main car must be in the first column
            raise ValueError(f"Main car '{main_sym}' must start on first column (col 0), got col {main_car['col0']}")
        if goal_r != main_car["row0"]: # goal must be in the same row of the horizontal main car
            raise ValueError("Goal 'Z' must be on the same row as the main car (horizontal case)")
        if goal_c != N - 1: # the goal must be on the last column, if the main car is horizontal
            raise ValueError(f"Goal 'Z' must be on last column (col {N-1}) for horizontal main car, got col {goal_c}")
    else:
        if main_car["row0"] != 0:
            raise ValueError(f"Main car '{main_sym}' must start on first row (row 0), got row {main_car['row0']}")
        if goal_c != main_car["col0"]:
            raise ValueError("Goal 'Z' must be on the same column as the main car (vertical case)")
        if goal_r != N - 1:
            raise ValueError(f"Goal 'Z' must be on last row (row {N-1}) for vertical main car, got row {goal_r}")

    # No other car besides the main car should be in the same lane (row/col) as itself
    if main_car["ori"] == "H":
        main_row = main_car["row0"] # row that the (head of the) main car occupies
        for i, c in enumerate(cars): # Same as "for i in range(len(cars)):\n c = cars[i]", but shorter
            if i == main_index: # Let's skip checking the main car against itself
                continue
            if c["ori"] == "H" and c["row0"] == main_row:
                raise ValueError("Another horizontal car shares the main car's row (forbidden)")
    else:
        main_col = main_car["col0"]
        for i, c in enumerate(cars):
            if i == main_index:
                continue
            if c["ori"] == "V" and c["col0"] == main_col:
                raise ValueError("Another vertical car shares the main car's column (forbidden)")

    return cars, main_index, (goal_r, goal_c)


# --------------------------------------------------------------------------------------------------
# 3) Z3 planning model
# --------------------------------------------------------------------------------------------------

def build_planning_solver(N, cars, main_index, goal, T, exactly_one_moves=True, dump_smt2=False):
    K = len(cars) # total number of cars (main car + obstacles)
    goal_r, goal_c = goal # grab the goal cell coordinates

    s = Solver() # Z3 solver instance

    row = [[Int(f"r_{i}_{t}") for t in range(T + 1)] for i in range(K)]
    col = [[Int(f"c_{i}_{t}") for t in range(T + 1)] for i in range(K)]
    moves = [[Bool(f"move_{i}_{t}") for t in range(T)] for i in range(K)] # the bool for the transition (t -> t+1)

    # X B B X X
    # X X b X X
    # P X b X Z
    # X X X X X
    # A A A X X

    # cars = [
    #    {  # cars[0]
    #        "name": "C1",
    #        "ori": "H",
    #        "len": 2,
    #        "row0": 0,
    #        "col0": 1,
    #        "symbol": "B"
    #    },
    #    {  # cars[1]
    #        "name": "C2",
    #        "ori": "V",
    #        "len": 2,
    #        "row0": 1,
    #        "col0": 2,
    #        "symbol": "b"
    #    },
    #    {  # cars[2] (MAIN CAR)
    #        "name": "P",
    #        "ori": "H",
    #        "len": 1,
    #        "row0": 2,
    #        "col0": 0,
    #        "symbol": "P"
    #    },
    #    {  # cars[3]
    #        "name": "C3",
    #        "ori": "H",
    #        "len": 3,
    #        "row0": 4,
    #        "col0": 0,
    #        "symbol": "A"
    #    }
    # ]
    # main_index = 2
    # goal = (2, 4)
    
    # To simplify:
    # index = 0, car B, (row[0][0], col[0][0]) = (0,1)
    # index = 1, car b, (row[1][0], col[1][0]) = (1,2), which means: car with index [1] at time [0] is in (1,2)
    # index = 2, car P, (row[2][0], col[2][0]) = (2,0)
    # index = 3, car A, (row[3][0], col[3][0]) = (4,0)

    # So, the main car 'P' with index [2] at a certain time [T] is in position (2,4), which is the GOAL
    # row[2][T] == 2, col[2][T] == 4

    # ********* Initial positions: *********
    for i, c in enumerate(cars): # Same as "for i in range(len(cars)):\n c = cars[i]", but shorter
        s.add(row[i][0] == c["row0"]) # car with index [i] at time [0] is in the same row as the head of that car
        s.add(col[i][0] == c["col0"]) # car with index [i] at time [0] is in the same col as the head of that car

    # ********* Boundaries: *********
    for i, c in enumerate(cars):
        L = c["len"] # length of the car with index [i]
        ori = c["ori"] # orientation of the car with index [i]
        for t in range(T + 1):
            # From t=0 up until t=(3+1), excluding. If we allow T moves, then we have to represent T+1 states.
            # Example: t=0 -> move 1 -> t=1 -> move 2 -> t=2 -> move 3 -> t=3 (3 moves, 4 states).
            s.add(And(0 <= row[i][t], row[i][t] < N)) # Both the head and the tail of each car can't go out of bounds
            s.add(And(0 <= col[i][t], col[i][t] < N))
            if ori == "H":
                s.add(col[i][t] + L - 1 < N) # Head + len = tail index, which must be less than the size of the board
            else:
                s.add(row[i][t] + L - 1 < N)

    # ********* Motion (left, right, up, down, stay) and "Did the car move?" and Define Moves: *********
    for i, c in enumerate(cars):
        ori = c["ori"]
        for t in range(T):
            if ori == "H":
                s.add(Or(
                    And(row[i][t + 1] == row[i][t], col[i][t + 1] == col[i][t]), # Stay in the same place
                    And(row[i][t + 1] == row[i][t], col[i][t + 1] == col[i][t] + 1), # Move right one cell
                    And(row[i][t + 1] == row[i][t], col[i][t + 1] == col[i][t] - 1), # Move left one cell
                ))
            else:
                s.add(Or(
                    And(col[i][t + 1] == col[i][t], row[i][t + 1] == row[i][t]), # Stay in the same place
                    And(col[i][t + 1] == col[i][t], row[i][t + 1] == row[i][t] + 1), # Move down once cell
                    And(col[i][t + 1] == col[i][t], row[i][t + 1] == row[i][t] - 1), # Move up one cell
                ))

            s.add(moves[i][t] == Or(row[i][t + 1] != row[i][t], col[i][t + 1] != col[i][t])) # True if either "row" or "col" of the car at index [i] change between t to t+1. (moves[i][t] is True if the car moved)

    # "At most one car moves per step" + "At least one car moves per step" = "Exactly one car moves per step"
    for t in range(T): # from t=0 till t=T, excluding.
        # At most one car moves at step t:
        for i in range(K):
            for j in range(i + 1, K): # For each fixed i, j goes from i+1 till K, excluded.
                s.add(Or(Not(moves[i][t]), Not(moves[j][t])))
                # Example for K=4 (cars 0,1,2,3):
                # And(Or(Not(moves[0][t]), Not(moves[1][t]))), Or(Not(moves[0][t]), Not(moves[2][t]))), ...)
                # (Either "Car 0 doesn't move" or "Car 1 doesn't move") And (Either "Car 1 doesn't move" or "Car 2 doesn't move") And ... 
                # (!0 v !1) ^ (!0 v !2) ^ (!0 v !3) ^ (!1 v !2) ^ (!1 v !3) ^ (!2 v !3) =
                # !(0 ∧ 1) ∧ !(0 ∧ 2) ∧ !(0 ∧ 3) ∧ !(1 ∧ 2) ∧ !(1 ∧ 3) ∧ !(2 ∧ 3)
                # So two different cars cannot both have "moves[*][t] = True"
        # At least one car moves at step t:
        if exactly_one_moves:
            s.add(Or([moves[i][t] for i in range(K)]))
            # 0 v 1 v 2 v 3

    # ********* Collisions (no overlapping cars): *********
    def car_cell(row_it, col_it, ori, length, segment_index):
        return (row_it, col_it + segment_index) if ori == "H" else (row_it + segment_index, col_it)
        # segment_index = 0 -> head
        # segment_index = 1 -> next cell

    for t in range(T + 1): # Check collisions for every state t = 0..T-1, exclusive.
        for i in range(K): # Fix the first car index i.
            for j in range(i + 1, K): # Compare car i with other cars after it
                # 0 with 1, 0 with 2, 0 with 3, 1 with 2, 1 with 3, 2 with 3
                ori_i, L_i = cars[i]["ori"], cars[i]["len"]
                ori_j, L_j = cars[j]["ori"], cars[j]["len"]
                for si in range(L_i): # Iterate over every segment of car i
                    # Example: if L_i = 3, si = 0,1,2 (head, middle, tail)
                    # Car i segments: (i,0), (i,1), (i,2)
                    r_i, c_i = car_cell(row[i][t], col[i][t], ori_i, L_i, si) # Compute the (row, col) of segment si of car i at time t
                    for sj in range(L_j): # Iterate over every segment of car j
                        # Example: if L_j = 2, sj = 0,1
                        # Car j segments: (j,0), (j,1)
                        r_j, c_j = car_cell(row[j][t], col[j][t], ori_j, L_j, sj) # Compute the (row, col) of segment sj of car j at time t
                        s.add(Or(r_i != r_j, c_i != c_j)) # It takes only one different row or column to not collide
                        # Example:
                        # 
                        # A A A
                        # X b X
                        # X b X
                        # 
                        # We check:
                        # (0,0) = A compared with (1,1) = b,
                        # (0,0) = A compared with (2,1) = b,
                        # (0,1) = A compared with (1,1) = b,
                        # (0,1) = A compared with (2,1) = b,
                        # (0,2) = A compared with (1,1) = b,
                        # (0,2) = A compared with (2,1) = b,
                        # If there's at least one different column or row for each comparison, then there is no collision

    # ********* Goal *********
    # "At time T, the main car must be at the goal cell". If the main car reaches the goal earlier, it is allowed to remain there for the remaining steps, since "stay in place" is a valid move.
    # When exactly_one_moves=True, the solver is not allowed to have idle steps: at every time step, some car must move. Because of this, once the main car reaches the goal, other cars may still perform unnecessary back-and-forth moves just to satisfy this constraint.
    # This behavior is intentional: enforcing exactly one move per step prevents idle padding (where no car moves) before the goal is reached. The issue of extra moves after reaching the goal is handled later by searching for the minimal T, as we will see in the next function "find_minimal_plan" where we will check if there's a solution for T=0..max_T and the smallest number of steps is the correct minimal solution.
    s.add(row[main_index][T] == goal_r)
    s.add(col[main_index][T] == goal_c)

    if dump_smt2:
        os.makedirs("outputs", exist_ok=True)
        with open(f"outputs/model_dump_T{T}.smt2", "w") as f:
            f.write(s.to_smt2())

    return s, row, col

# Z3 by itself is just a satisfiability solver (SAT/UNSAT), not a shortest-path solver, so we do this:
# Try solving it with T=0 moves; if UNSAT, try T=1 move; if UNSAT, try T=2 moves; ...; first SAT T we find is garanteed to be minimal, because all smaller T failed
def find_minimal_plan(N, cars, main_index, goal, max_T=10, exactly_one_moves=True, dump_smt2=False):
    for T in range(max_T + 1): # T ranges from 0 to max_T, inclusive.
        s, row, col = build_planning_solver(N, cars, main_index, goal, T, exactly_one_moves=exactly_one_moves, dump_smt2=dump_smt2) # build_planning_solver creates variables row[i][t], col[i][t] for t=0..T and adds all constraints (initial positions, bounds, motion, collision, goal)
        if s.check() == sat: # Z3 checks if there exists an assignment of all row/col variables that satisfies the contraints we set. If SAT, we can extract a model which gives us values of all variables (positions of every car at every time)
            return T, s.model(), row, col
    return None # If this line is reached, then for every T <= max_T the problem was UNSAT, meaning no solution was found within max_T moves


# --------------------------------------------------------------------------------------------------
# 4) Rendering
# --------------------------------------------------------------------------------------------------

def ordinal(k): # Converts: 1 -> "first", 2 -> "second", ..., 11 -> "11th"
    mapping = {
        1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth",
        6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth"
    }
    return mapping.get(k, f"{k}th")

# Returns the short solution list, for example, "P right one cell", "b up one cell", ...
# The "dr" is the row change (up/down) and the "dc" is the column change (left/right)
# dr = r_curr - r_prev (down=+1, up=-1), dc = c_curr - c_prev (right=+1, left=-1).
def move_phrase(car, dr, dc):
    sym = car["symbol"]
    if car["ori"] == "H":
        if dc == 1:
            return f"{sym} right one cell"
        if dc == -1:
            return f"{sym} left one cell"
    else:
        if dr == 1:
            return f"{sym} down one cell"
        if dr == -1:
            return f"{sym} up one cell"
    return None


def move_sentence(car, dr, dc): # Similar to the previous function, but sounds more natural. I might get rid of this
    sym = car["symbol"]
    if car["ori"] == "H":
        if dc == 1:
            return f"{sym} moves right one cell"
        if dc == -1:
            return f"{sym} moves left one cell"
    else:
        if dr == 1:
            return f"{sym} moves down one cell"
        if dr == -1:
            return f"{sym} moves up one cell"
    return None

# Renders a board state at a given time step using the Z3 model.
# It places every car on a NxN grid based on it's head position, orientation and length.
# It fills empty cells with "X", and highlights the goal cell using brackets ([X])
#
# row_vars_at_t and col_vars_at_t are lists of Z3 variables, one per car, already fixed to a single time step t.
# For example, in the function ahead "print_puzzle_and_solution" the call [row_vars[i][0] for i in range(K)] passes the row positions of all cars at time t = 0.
# render_board does not know what t is; it simply draws the board using the positions it is given.
def render_board(N, cars, row_vars_at_t, col_vars_at_t, model, goal):
    goal_r, goal_c = goal
    grid = [[None for _ in range(N)] for __ in range(N)]
    # For example:
    # [
    #  [None, None, None],
    #  [None, None, None],
    #  [None, None, None]
    # ]
    # The cells are empty for now. Later, cars overwrite these cells with "P", "A", "b", etc. Any cell still "None" at the end becomes "X" when printed (empty)

    def val(x): # Z3 variables are symbolic (e.g. r_2_3 = "row of car 2 at time 3"). This function asks the Z3 model for the concrete value assigned to x and converts it into a normal python integer (e.g. r_2_3 -> 4)
        return model.evaluate(x).as_long()

    for i, car in enumerate(cars):
        ori = car["ori"]
        L = car["len"]
        sym = car["symbol"]
        r0 = val(row_vars_at_t[i]) # head row at this time step
        c0 = val(col_vars_at_t[i]) # head column at this time step
        for k in range(L): # Fill head until tail cells
            r = r0 if ori == "H" else r0 + k
            c = c0 + k if ori == "H" else c0
            grid[r][c] = sym

    lines = []
    for r in range(N):
        cells = []
        for c in range(N):
            char = grid[r][c] if grid[r][c] is not None else "X" # Empty cells become "X"
            cell_str = f"[{char}]" if (r, c) == (goal_r, goal_c) else f" {char} " # If the current cell (r,c) is the goal cell, print inside brackets like [X] or [P], otherwise print it normally like " X " or " P ".
            cells.append(cell_str) # Adds the cell's printed string into the current row list
            # Example: [" X ", " P ", " X ", " X ", "[X]"]
        lines.append("".join(cells)) # concatenates all the cell strings into one single string
    return "\n".join(lines) # puts a new line (\n) between each row string
    # "lines" ends up looking like this:
    # X  X  X  X  X
    # X  X  X  X  X
    # P  X  X  X [X]
    # X  X  X  X  X
    # X  X  X  X  X

def print_puzzle_and_solution(title, N, cars, main_index, goal, T, model, row_vars, col_vars):
    K = len(cars)
    goal_r, goal_c = goal

    def val(x):
        return model.evaluate(x).as_long()

    # Print puzzle title and initial board configuration (time t = 0)
    print(title)
    board_t0 = render_board(
        N, cars,
        [row_vars[i][0] for i in range(K)],
        [col_vars[i][0] for i in range(K)],
        model, goal=(goal_r, goal_c)
    )
    print(board_t0)

    solution_steps = [] # List of short move descriptions (for final summary)

    # Iterate through each time step of the solution
    for t in range(1, T + 1):
        step_move_sentences = [] # Human-readable descriptions for this step
        for i, car in enumerate(cars): # Check each car to see if it moved between t-1 and t
            r_prev = val(row_vars[i][t - 1])
            c_prev = val(col_vars[i][t - 1])
            r_curr = val(row_vars[i][t])
            c_curr = val(col_vars[i][t])
            dr = r_curr - r_prev # Row displacement
            dc = c_curr - c_prev # Column displacement
            if dr == 0 and dc == 0: # If the car did not move, skip it
                continue

            # Build natural-language and short-form descriptions
            sent = move_sentence(car, dr, dc)
            phr = move_phrase(car, dr, dc)
            if sent is not None:
                step_move_sentences.append(sent)
            if phr is not None:
                solution_steps.append(phr)

        # Summary of moves at this step (should be exactly one unless idle steps are allowed)
        inside = ", ".join(step_move_sentences) if step_move_sentences else "no car moves"

        # Print the board after the current move
        print()
        print(f"Puzzle, {ordinal(t)} move ({inside}):")
        board_t = render_board(
            N, cars,
            [row_vars[i][t] for i in range(K)],
            [col_vars[i][t] for i in range(K)],
            model, goal=(goal_r, goal_c)
        )
        print(board_t)

    # Final summary
    print()
    print(f"Puzzle resolved in {T} moves.")
    if solution_steps:
        print(f"Solution: {', '.join(solution_steps)}")
    else:
        print("Solution: (no moves needed – already at goal)")


# --------------------------------------------------------------------------------------------------
# 5) CLI / interactive selection
# --------------------------------------------------------------------------------------------------

def list_txt_puzzles_in_cwd(): # Return all .txt files in the current directory, sorted alphabetically
    return sorted([f for f in os.listdir(".") if os.path.isfile(f) and f.lower().endswith(".txt")])


def prompt_int(prompt, default): # Prompt the user for an integer, falling back to a default if input is empty
    raw = input(f"{prompt} [{default}]: ").strip()
    if raw == "":
        return default
    return int(raw)


def prompt_str(prompt, default): # Prompt the user for a string, falling back to a default if input is empty
    raw = input(f"{prompt} [{default}]: ").strip()
    if raw == "":
        return default
    return raw


def interactive_choose_mode(): # Ask the user whether to generate a puzzle or load one from a file
    print("Choose puzzle source:")
    print("  1) Generate random puzzle")
    print("  2) Use existing manual puzzle (.txt in this directory)")
    while True:
        ans = input("Enter 1 or 2: ").strip()
        if ans in ("1", "2"):
            return int(ans)


def interactive_pick_file(): # Let the user select a .txt puzzle file from the current directory
    files = list_txt_puzzles_in_cwd()
    if not files:
        print("No .txt puzzle files found in the current directory.")
        return None

    print("\nAvailable puzzle files:")
    for i, f in enumerate(files, 1):
        print(f"  {i}) {f}")

    while True:
        raw = input("Pick a file by number (or type a filename): ").strip()
        if raw == "":
            continue
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(files):
                return files[idx - 1]
            print("Invalid number.")
        else:
            if os.path.isfile(raw):
                return raw
            print("File not found.")


def main(): # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate or solve car-movement puzzles.")
    parser.add_argument("--file", help="Solve a manual puzzle from this .txt file (skips interactive prompt)")
    parser.add_argument("--generate", action="store_true", help="Generate a random puzzle (skips interactive prompt)")
    parser.add_argument("--maxT", type=int, default=10, help="Maximum number of moves to search")
    parser.add_argument("--idle-ok", action="store_true", help="Allow steps where no car moves (removes 'exactly one car moves' constraint)")
    parser.add_argument("--dump-smt2", action="store_true", help="Dump SMT-LIB2 (.smt2) encoding of the planning problem to outputs/")
    args = parser.parse_args()
    dump_smt2 = args.dump_smt2
    
    exactly_one_moves = not args.idle_ok

    # Decide which mode to run
    if args.file and args.generate:
        print("Error: use either --file or --generate, not both.")
        sys.exit(1)

    if args.file:
        mode = 2
    elif args.generate:
        mode = 1
    else:
        mode = interactive_choose_mode()

    # Load and solve a manual puzzle
    if mode == 2:
        filename = args.file if args.file else interactive_pick_file()
        if not filename:
            return

        try:
            grid = read_grid_from_file(filename)
        except Exception as e:
            print(f"Error reading puzzle file: {e}")
            return

        N = len(grid)

        try:
            cars, main_index, goal = validate_and_build_cars(grid)
        except ValueError as e:
            print(f"Puzzle is NOT valid: {e}")
            return

        result = find_minimal_plan(N, cars, main_index, goal, max_T=args.maxT, exactly_one_moves=exactly_one_moves, dump_smt2=dump_smt2)
        if result is None:
            print("Puzzle is valid, but no solution found within the given move limit.")
            return

        T, model, row_vars, col_vars = result
        print_puzzle_and_solution("Puzzle is valid.\n\nPuzzle:", N, cars, main_index, goal, T, model, row_vars, col_vars)

    else:
        # Interactive random puzzle generation
        print("\nRandom puzzle generation parameters (press Enter for defaults):")
        N = prompt_int("Board size N", 5)
        num_obstacles = prompt_int("Number of obstacle cars", 4)
        main_orientation = prompt_str("Main car orientation (H or V)", "H").upper()
        if main_orientation not in ("H", "V"):
            print("Invalid orientation; must be H or V.")
            return
        max_car_len = prompt_int("Max obstacle car length", min(3, N))
        seed_raw = input("Random seed (blank for None): ").strip()
        seed = None if seed_raw == "" else int(seed_raw)

        try:
            cars, goal = generate_random_board(N, num_obstacles=num_obstacles, main_orientation=main_orientation, max_car_len=max_car_len, seed=seed)
        except Exception as e:
            print(f"Error generating puzzle: {e}")
            return

        main_index = 0 # Main car is always the first car when generating randomly

        result = find_minimal_plan(N, cars, main_index, goal, max_T=args.maxT, exactly_one_moves=exactly_one_moves, dump_smt2=dump_smt2)
        if result is None:
            print(f"No plan found up to T = {args.maxT}")
            return

        T, model, row_vars, col_vars = result
        print_puzzle_and_solution("Generated puzzle:", N, cars, main_index, goal, T, model, row_vars, col_vars)


if __name__ == "__main__":
    main()