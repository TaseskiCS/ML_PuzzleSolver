import heapq
import random

# Defines the initial state of the puzzle
START_STATE = [ 
    [4, 2, 3, 7],
    [1, 13, 10, 6],
    [8, 5, 9, 11],
    [12, 0, 14, 15]
]

GOAL_STATE = [ 
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [8, 9, 10, 11],
    [12, 13, 14, 15]
]

# Variable to increase size of game
SIZE = 4

# This is our heuristic 1 Count the number of misplaced tiles 
def heuristic1(state, goal_state):
    steps = 0
    for x in range(len(state)):
        for y in range(len(state[x])):
            # If the tile is not in its goal position and is not the empty tile, increment steps
            if state[x][y] != goal_state[x][y] and state[x][y] != 0:
                steps += 1
    return steps

# This is our heuristic 2 Calculate the Manhattan Distance of each tile from its goal position
def heuristic2(state, goal_state):
    map_goal = {}  
    distance = 0

    for x in range(len(goal_state)):
        for y in range(len(goal_state[x])):
            map_goal[goal_state[x][y]] = (x, y)

    for x in range(len(state)):
        for y in range(len(state[x])):
            value = state[x][y]
            if value != 0:
                goal_x, goal_y = map_goal[value]
                distance += abs(x - goal_x) + abs(y - goal_y)

    return distance

# heuristic 3 to Count the number of tiles not in their correct row
def heuristic3(state, goal_state):
    misplaced = 0
    for x in range(SIZE):
        for y in range(SIZE):
            if state[x][y] != 0 and state[x][y] not in goal_state[x]:
                misplaced += 1
    return misplaced

# Function to find the position of the empty tile (0)
def find_zero(state):
    for x in range(len(state)):
        for y in range(len(state[x])):
            if state[x][y] == 0:
                return x, y

# Function to generate a new puzzle state by making random moves
def generate_puzzles(state, moves=30) -> list:
    moves_dic = {'left': [0, -1], 'right': [0, 1], 'up': [-1, 0], 'down': [1, 0]}
    new_state = [row[:] for row in state]  
    
    for _ in range(moves):
        zero_x, zero_y = find_zero(new_state)
        valid_moves = []
        
        # checks all possible moves and keep only the valid ones
        for direction, (dx, dy) in moves_dic.items():
            new_x, new_y = zero_x + dx, zero_y + dy
            if 0 <= new_x < SIZE and 0 <= new_y < SIZE:
                valid_moves.append((new_x, new_y))
        
        # if there are good moves, randomly choose one and swap the tiles
        if valid_moves:
            new_x, new_y = random.choice(valid_moves)
            new_state[zero_x][zero_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[zero_x][zero_y]
            
    return new_state

# Function to generate 100 unique puzzle states
def generate_100_puzzles():
    puzzles = set()  # Use a set to store unique puzzle states
    while len(puzzles) < 100:
        puzzle = generate_puzzles(GOAL_STATE, moves=30)
        puzzles.add(tuple(map(tuple, puzzle)))  # Convert the puzzle to a tuple of tuples for hashing

    return [list(map(list, puzzle)) for puzzle in puzzles]  # Convert back to a list of lists

# A* search algorithm
def a_star(start_state, goal_state, use_heuristic=1):
    match use_heuristic:
        case 1:
            heuristic = heuristic1
        case 2:
            heuristic = heuristic2
        case _:
            heuristic = heuristic3

    #heuristic = heuristic2 if use_heuristic2 else heuristic1
    start_tuple = tuple(map(tuple, start_state))
    goal_tuple = tuple(map(tuple, goal_state))
    open_set = []
    heapq.heappush(open_set, (heuristic(start_state, goal_state), 0, start_tuple, []))  
    visited = set()  
    
    # Define the possible moves
    moves = {'left': [0, -1], 'right': [0, 1], 'up': [-1, 0], 'down': [1, 0]}
    
    while open_set:
        _, g, current, path = heapq.heappop(open_set)
        if current == goal_tuple:
            return path, len(visited)
        if current in visited:
            continue
        visited.add(current)
        zero_x, zero_y = find_zero([list(row) for row in current])
        
        # Generate all possible next states by moving the empty tile
        for move in moves.values():
            new_x, new_y = zero_x + move[0], zero_y + move[1]
            if 0 <= new_x < SIZE and 0 <= new_y < SIZE:
                new_state = [list(row) for row in current]
                new_state[zero_x][zero_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[zero_x][zero_y]
                neighbor_tuple = tuple(map(tuple, new_state))
                if neighbor_tuple not in visited:
                    new_path = path + [new_state]
                    heapq.heappush(open_set, (g + 1 + heuristic(new_state, goal_state), g + 1, neighbor_tuple, new_path))
    
    # If no solution is found, return None
    return None

# The main block of code to run the program 
def main():

    #Initialize Total Solution lengths and visited lengths over 100 puzzles
    total_length_h1 = 0
    total_length_h2 = 0
    total_length_h3 = 0

    total_nodes_h1 = 0
    total_nodes_h2 = 0
    total_nodes_h3 = 0

    # To Generate 100 Random Puzzle States
    puzzles = generate_100_puzzles()
    print("Generated 100 Random Puzzle States:")
    for i, puzzle in enumerate(puzzles, 1):
        print(f"Puzzle {i}:")
        for row in puzzle:
            print(row)
        print()
    
        # This is to solve the puzzle using A* wth heuristic 1 
        solution_path_h1, visited_len_h1 = a_star(puzzle, GOAL_STATE, use_heuristic=1)
        if solution_path_h1:
            print(f"Solution found in {len(solution_path_h1)} moves Using H1:")
            total_length_h1 += heuristic1(puzzle, GOAL_STATE)
            total_nodes_h1 += visited_len_h1
            # for step, state in enumerate(solution_path_h1, 1):
            #     print(f"Step {step}:")
            #     for row in state:
            #         print(row)
            #     print()
        else:
            print("No solution found.")
        print()

        # This is to solve the puzzle using A* wth heuristic 2
        solution_path_h2, visited_len_h2 = a_star(puzzle, GOAL_STATE, use_heuristic=2)
        if solution_path_h2:
            print(f"Solution found in {len(solution_path_h2)} moves Using H2:")
            total_length_h2 += heuristic2(puzzle, GOAL_STATE)
            total_nodes_h2 += visited_len_h2
            # for step, state in enumerate(solution_path_h2, 1):
            #     print(f"Step {step}:")
            #     for row in state:
            #         print(row)
            #     print()
        else:
            print("No solution found.")
        print()

        # This is to solve the puzzle using A* wth heuristic 2
        solution_path_h3, visited_len_h3 = a_star(puzzle, GOAL_STATE, use_heuristic=3)
        if solution_path_h3:
            print(f"Solution found in {len(solution_path_h3)} moves Using H3:")
            total_length_h3 += heuristic3(puzzle, GOAL_STATE)
            total_nodes_h3 += visited_len_h3
            # for step, state in enumerate(solution_path_h3, 1):
            #     print(f"Step {step}:")
            #     for row in state:
            #         print(row)
            #     print()
        else:
            print("No solution found.")
        print()
        print()

    # Find Average Lengths
    avg_length_h1 = total_length_h1 / 100
    avg_length_h2 = total_length_h2 / 100
    avg_length_h3 = total_length_h3 / 100

    avg_nodes_h1 = total_nodes_h1 / 100
    avg_nodes_h2 = total_nodes_h3 / 100
    avg_nodes_h3 = total_nodes_h3 / 100

    # printing the heuristic values 
    print("\nHeuristic 1 Steps Needed:", heuristic1(START_STATE, GOAL_STATE))
    print("Heuristic 2 Steps Needed:", heuristic2(START_STATE, GOAL_STATE))
    print("Heuristic 3 Steps Needed:", heuristic3(START_STATE, GOAL_STATE))
    print()
    print(f"15-Puzzle  h1  {avg_length_h1:<4}  {avg_nodes_h1}")
    print(f"15-Puzzle  h2  {avg_length_h2:<4}  {avg_nodes_h2}")
    print(f"15-Puzzle  h3  {avg_length_h3:<4}  {avg_nodes_h3}")

if __name__ == "__main__":
    main()