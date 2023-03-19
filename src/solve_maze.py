import json
from collections import deque
import heapq
from datetime import datetime
import argparse

from create_maze import create_canvas, draw_maze

RES_DIR_PATH = '../res'
MAZE_FILE_PATH = f'{RES_DIR_PATH}/maze.json'
CONFIG_FILE_PATH = f'{RES_DIR_PATH}/config.json'

def load_maze(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data['grid'], data['start'], data['end']

def load_config(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data

def get_unwalled_neighbors(maze, x, y):
    neighbors = []
    
    # For each possible neighbor, check if there is a wall between the current cell and the neighbor
    for dx, dy, wall1, wall2 in [(-1, 0, 'left', 'right'), (0, -1, 'top', 'bottom'), (1, 0, 'right', 'left'), (0, 1, 'bottom', 'top')]:
        
        # If there is no wall between the current cell and the neighbor, and the neighbor is within the bounds of the maze, add it to the list of neighbors
        if not maze[x][y][wall1]:
            if 0 <= x + dx < len(maze) and 0 <= y + dy < len(maze) and not maze[x+dx][y+dy][wall2]:
                neighbors.append((x + dx, y + dy))
                
    return neighbors

# @profile
def depth_first_search(maze, start, end):
    start_time = datetime.now()  # Start time
    
    visited = set()
    stack = [(start, [start])]
    nodes_visited = 0  # Number of nodes visited
    
    while stack:
        (x, y), path = stack.pop()
        
        if (x, y) == tuple(end):
            end_time = datetime.now()  # End time
            time_complexity = end_time - start_time  # Time complexity
            return path, time_complexity, nodes_visited
        
        if (x, y) not in visited:
            visited.add((x, y))
            nodes_visited += 1
            
            for neighbor_x, neighbor_y in get_unwalled_neighbors(maze, x, y):
                stack.append(((neighbor_x, neighbor_y), path + [(neighbor_x, neighbor_y)]))
                
    return None, None, nodes_visited

# @profile
def breadth_first_search(maze, start, end):
    start_time = datetime.now()  # Start time
    
    visited = set()
    queue = deque([(start, [start])])
    nodes_visited = 0  # Number of nodes visited
    
    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == tuple(end):
            end_time = datetime.now()  # End time
            time_complexity = end_time - start_time  # Time complexity
            return path, time_complexity, nodes_visited
        
        if (x, y) not in visited:
            visited.add((x, y))
            nodes_visited += 1
            
            for neighbor_x, neighbor_y in get_unwalled_neighbors(maze, x, y):
                queue.append(((neighbor_x, neighbor_y), path + [(neighbor_x, neighbor_y)]))
                
    return None, None, nodes_visited

def heuristic(x, y, end):
    return abs(x - end[0]) + abs(y - end[1])

# @profile
def a_star(maze, start, end):
    start_time = datetime.now()  # Start time

    visited = set()
    heap = [(heuristic(start[0], start[1], end), 0, start, [start])]
    nodes_visited = 0  # Number of nodes visited
    
    while heap:
        _, cost, (x, y), path = heapq.heappop(heap)
        
        if (x, y) == tuple(end):
            end_time = datetime.now()  # End time
            time_complexity = end_time - start_time  # Time complexity
            return path, time_complexity, nodes_visited
        
        if (x, y) not in visited:
            visited.add((x, y))
            nodes_visited += 1
            
            for neighbor_x, neighbor_y in get_unwalled_neighbors(maze, x, y):
                new_cost = cost + 1
                new_path = path + [(neighbor_x, neighbor_y)]
                heapq.heappush(heap, (new_cost + heuristic(neighbor_x, neighbor_y, end), new_cost, (neighbor_x, neighbor_y), new_path))
                
    return None, None, nodes_visited

def valid_actions(maze, s):
    x, y = s
    A = set()

    if y > 0 and not maze[x][y]['top']:
        A.add((0, -1))
    if y < len(maze[0]) - 1 and not maze[x][y]['bottom']:
        A.add((0, 1))
    if x > 0 and not maze[x][y]['left']:
        A.add((-1, 0))
    if x < len(maze) - 1 and not maze[x][y]['right']:
        A.add((1, 0))
        
    return A
    
def transition_prob(s_next, s, a):
    x, y = s
    dx, dy = a
    x_next, y_next = s_next

    if (x+dx, y+dy) == (x_next, y_next):
        return 1
    else:
        return 0
    
def reward(s, a):
    x, y = s
    dx, dy = a

    if (x+dx, y+dy) == tuple(end):
        return 100
    # elif (x+dx, y+dy) in visited:
    #     return -50  # Negative reward for revisiting a visited cell
    else:
        return -1

def path_from_policy(policy, start, end):
    s = tuple(start)
    path = []

    while s != tuple(end):
        a = policy[s]
        dx, dy = a
        s_next = (s[0] + dx, s[1] + dy)
        path.append(s_next)
        s = s_next

    return path

# @profile
def mdp_value_iteration(maze, start, end):
    start_time = datetime.now()  # Start time
    
    S = set((x, y) for x in range(len(maze)) for y in range(len(maze[0])))
    A = valid_actions
    P = transition_prob
    R = reward
    
    def value_iteration(S, A, P, R, gamma=0.9):
        V = {s: 0 for s in S}
        optimal_policy = {s: 0 for s in S}
        states_visited = []  # Number of states visited
        
        while True:
            states_visited_count = 0
            oldV = V.copy()

            for s in S:
                states_visited_count += 1
                
                Q = {}

                for a in A(maze, s):
                    Q[a] = R(s, a) + gamma * sum(P(s_next, s, a) * oldV[s_next] for s_next in S)

                V[s] = max(Q.values())
                optimal_policy[s] = max(Q, key=Q.get)
            
            states_visited.append(states_visited_count)
                
            if all(oldV[s] == V[s] for s in S):
                end_time = datetime.now()  # End time
                time_complexity = end_time - start_time  # Time complexity
                break

        return [tuple(start)] + path_from_policy(optimal_policy, start, end), time_complexity, states_visited
    
    path, time_complexity, states_visited = value_iteration(S, A, P, R)

    return path, time_complexity, states_visited

# @profile
def mdp_policy_iteration(maze, start, end):
    start_time = datetime.now()  # Start time
    
    S = set((x, y) for x in range(len(maze)) for y in range(len(maze[0])))
    A = valid_actions
    P = transition_prob
    R = reward
    
    def policy_evaluation(policy, S, P, R, gamma):
        V = {s: 0 for s in S}
        states_visited = []  # Number of states visited
        
        while True:
            states_visited_count = 0
            oldV = V.copy()

            for s in S:
                states_visited_count += 1
                
                a = policy[s]
                V[s] = R(s, a) + gamma * sum(P(s_next, s, a) * oldV[s_next] for s_next in S)
            
            states_visited.append(states_visited_count)

            if all(oldV[s] == V[s] for s in S):
                break
        
        return V, states_visited
    
    def policy_improvement(V, S, A, P, R, gamma):
        policy = {s: (0, 0) for s in S}

        for s in S:
            Q = {}

            for a in A(maze, s):
                Q[a] = R(s, a) + gamma * sum(P(s_next, s, a) * V[s_next] for s_next in S)
            
            policy[s] = max(Q, key=Q.get)
        
        return policy
    
    def policy_iteration(S, A, P, R, gamma=0.9):
        policy = {s: (0, 0) for s in S}
        states_visited = []  # Number of states visited
        
        while True:
            old_policy = policy.copy()

            V, states_visited_policy_evaluation = policy_evaluation(policy, S, P, R, gamma)
            states_visited += states_visited_policy_evaluation
            
            policy = policy_improvement(V, S, A, P, R, gamma)

            if all(old_policy[s] == policy[s] for s in S):
                end_time = datetime.now()  # End time
                time_complexity = end_time - start_time  # Time complexity
                break
        
        return [tuple(start)] + path_from_policy(policy, start, end), time_complexity, states_visited
    
    path, time_complexity, states_visited = policy_iteration(S, A, P, R)

    return path, time_complexity, states_visited

def print_path(path):
    if path is None:
        print("No path found!")
    else:
        print("Path found:")
        for x, y in path:
            print(f"({x}, {y})")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--algorithm', type=str, help='Select the maze solving algorithm: dfs, bfs, a_star, mdp_value, mdp_policy')
    args = parser.parse_args()

    grid, start, end = load_maze(MAZE_FILE_PATH)
    
    if args.algorithm == 'dfs':
        path, tc, v = depth_first_search(grid, start, end)
    elif args.algorithm == 'bfs':
        path, tc, v = breadth_first_search(grid, start, end)
    elif args.algorithm == 'a_star':
        path, tc, v = a_star(grid, start, end)
    elif args.algorithm == 'mdp_value':
        path, tc, v = mdp_value_iteration(grid, start, end)
    elif args.algorithm == 'mdp_policy':
        path, tc, v = mdp_policy_iteration(grid, start, end)
    else:
        print('Invalid algorithm selected!')
        exit()

    print(f'Time Complexity: {tc}')
    
    if isinstance(v, list):
        print(f'Iterations: {len(v)}')
    else:
        print(f'Nodes Visited: {v}')
    
    config_data = load_config(CONFIG_FILE_PATH)
    grid_size = config_data["grid_size"]
    cell_size = config_data["cell_size"]

    # Create the canvas
    window, canvas = create_canvas(grid_size, cell_size)

    # Draw the maze on the canvas
    draw_maze(canvas, cell_size, grid_size, grid, start, end, path=path)

    # Start the main tkinter loop
    window.mainloop()