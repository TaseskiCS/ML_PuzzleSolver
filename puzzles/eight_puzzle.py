import heapq
import random

START_STATE = [ 
    [7, 2, 4],
    [5, 0, 6],
    [8, 3, 1]
]

GOAL_STATE = [ 
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

def heuristic1(state, goal_state):
    steps = 0
    for x in range(len(state)):
        for y in range(len(state[x])):
            if state[x][y] != goal_state[x][y] and state[x][y] != 0:
                steps += 1
    return steps

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

def find_zero(state):
    for x in range(len(state)):
        for y in range(len(state[x])):
            if state[x][y] == 0:
                return x, y

def generate_puzzles(state, moves=30) -> list:
    moves_dic = {'left': [0, -1], 'right': [0, 1], 'up': [-1, 0], 'down': [1, 0]}
    new_state = [row[:] for row in state]
    
    for _ in range(moves):
        zero_x, zero_y = find_zero(new_state)
        valid_moves = []
        
        for direction, (dx, dy) in moves_dic.items():
            new_x, new_y = zero_x + dx, zero_y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                valid_moves.append((new_x, new_y))
        
        if valid_moves:
            new_x, new_y = random.choice(valid_moves)
            new_state[zero_x][zero_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[zero_x][zero_y]
            
    return new_state

def generate_100_puzzles():
    puzzles = set()
    while len(puzzles) < 100:
        puzzle = generate_puzzles(GOAL_STATE, moves=30)
        puzzles.add(tuple(map(tuple, puzzle)))

    return [list(map(list, puzzle)) for puzzle in puzzles]

def a_star(start_state, goal_state, use_heuristic2=True):
    heuristic = heuristic2 if use_heuristic2 else heuristic1
    
    start_tuple = tuple(map(tuple, start_state))
    goal_tuple = tuple(map(tuple, goal_state))
    
    open_set = []  # initialize priority queue (min-heap)
    heapq.heappush(open_set, (heuristic(start_state, goal_state), 0, start_tuple, []))  # (f, g, state, path)
    visited = set()
    
    moves = {'left': [0, -1], 'right': [0, 1], 'up': [-1, 0], 'down': [1, 0]}
    
    while open_set:
        _, g, current, path = heapq.heappop(open_set)

        if current == goal_tuple:
            return path  # we found the solution

        if current in visited:
            continue
        visited.add(current)

        zero_x, zero_y = find_zero([list(row) for row in current])
        
        for move in moves.values():
            new_x, new_y = zero_x + move[0], zero_y + move[1]
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = [list(row) for row in current]
                new_state[zero_x][zero_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[zero_x][zero_y]
                neighbor_tuple = tuple(map(tuple, new_state))
                
                if neighbor_tuple not in visited:
                    new_path = path + [new_state]
                    heapq.heappush(open_set, (g + 1 + heuristic(new_state, goal_state), g + 1, neighbor_tuple, new_path))
    
    return None  # if we didnt find a solution

def main():
    puzzles = generate_100_puzzles()
    print("Generated 100 Random Puzzle States:")
    for i, puzzle in enumerate(puzzles, 1):
        print(f"Puzzle {i}:")
        for row in puzzle:
            print(row)
        print()

        solution_path = a_star(puzzle, GOAL_STATE, use_heuristic2=True)
        if solution_path:
            print(f"Solution found in {len(solution_path)} moves:")
            for step, state in enumerate(solution_path, 1):
                print(f"Step {step}:")
                for row in state:
                    print(row)
                print()
        else:
            print("No solution found.")
    
    print("\nHeuristic 1 Steps Needed:", heuristic1(START_STATE, GOAL_STATE))
    print("Heuristic 2 Steps Needed:", heuristic2(START_STATE, GOAL_STATE))
if __name__ == "__main__":
    main()
    
    
