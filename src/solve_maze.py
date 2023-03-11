import json
from collections import deque
import heapq

from create_maze import create_canvas, draw_maze

RES_DIR_PATH = '../res'
MAZE_FILE_PATH = f'{RES_DIR_PATH}/maze.json'

def load_maze(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data['grid'], data['start'], data['end']

def get_unvisited_neighbors(maze, x, y):
    neighbors = []
    
    # For each possible neighbor, check if there is a wall between the current cell and the neighbor
    for dx, dy, wall1, wall2 in [(-1, 0, 'left', 'right'), (0, -1, 'top', 'bottom'), (1, 0, 'right', 'left'), (0, 1, 'bottom', 'top')]:
        
        # If there is no wall between the current cell and the neighbor, and the neighbor is within the bounds of the maze, add it to the list of neighbors
        if maze[x][y][wall1] == False:
            if 0 <= x + dx < len(maze) and 0 <= y + dy < len(maze) and maze[x+dx][y+dy][wall2] == False:
                neighbors.append((x + dx, y + dy, wall1, wall2))
                
    return neighbors

def depth_first_search(maze, start, end):
    visited = set()
    stack = [(start, [start])]
    
    while stack:
        (x, y), path = stack.pop()
        
        if (x, y) == tuple(end):
            return path
        
        if (x, y) not in visited:
            visited.add((x, y))
            
            for neighbor_x, neighbor_y, _, _ in get_unvisited_neighbors(maze, x, y):
                stack.append(((neighbor_x, neighbor_y), path + [(neighbor_x, neighbor_y)]))
                
    return None

def breadth_first_search(maze, start, end):
    visited = set()
    queue = deque([(start, [start])])
    
    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == tuple(end):
            return path
        
        if (x, y) not in visited:
            visited.add((x, y))
            
            for neighbor_x, neighbor_y, _, _ in get_unvisited_neighbors(maze, x, y):
                queue.append(((neighbor_x, neighbor_y), path + [(neighbor_x, neighbor_y)]))
                
    return None

def heuristic(x, y, end):
    return abs(x - end[0]) + abs(y - end[1])

def a_star(maze, start, end):
    visited = set()
    heap = [(heuristic(start[0], start[1], end), 0, start, [start])]
    
    while heap:
        _, cost, (x, y), path = heapq.heappop(heap)
        
        if (x, y) == tuple(end):
            return path
        
        if (x, y) not in visited:
            visited.add((x, y))
            
            for neighbor_x, neighbor_y, _, _ in get_unvisited_neighbors(maze, x, y):
                new_cost = cost + 1
                new_path = path + [(neighbor_x, neighbor_y)]
                heapq.heappush(heap, (new_cost + heuristic(neighbor_x, neighbor_y, end), new_cost, (neighbor_x, neighbor_y), new_path))
                
    return None

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

def mdp_value_iteration(maze, start, end):
    # visited = set()

    S = set((x, y) for x in range(len(maze)) for y in range(len(maze[0])))
    A = valid_actions
    P = transition_prob
    R = reward

    # https://www.youtube.com/watch?v=hUqeGLkx_zs
    def value_iteration(S, A, P, R, gamma=0.9):
        V = {s: 0 for s in S}
        optimal_policy = {s: 0 for s in S}

        while True:
            oldV = V.copy()

            for s in S:
                # visited.add(s)
                Q = {}

                for a in A(maze, s):
                    Q[a] = R(s, a) + gamma * sum(P(s_next, s, a) * oldV[s_next] for s_next in S)
                    
                V[s] = max(Q.values())
                optimal_policy[s] = max(Q, key=Q.get)
                
            if all(oldV[s] == V[s] for s in S):
                break
            # else:
            #     visited.clear()
            
        return V, optimal_policy
    
    V, optimal_policy = value_iteration(S, A, P, R)

    # Get the optimal path
    s = tuple(start)
    path = [s]
    while s != tuple(end):
        a = optimal_policy[s]
        dx, dy = a
        s_next = (s[0] + dx, s[1] + dy)
        path.append(s_next)
        s = s_next

    return path

def mdp_policy_iteration(maze, start, end):
    S = set((x, y) for x in range(len(maze)) for y in range(len(maze[0])))
    A = valid_actions
    P = transition_prob
    R = reward

    # https://www.youtube.com/watch?v=RlugupBiC6w
    def policy_evaluation(policy, S, P, R, gamma):
        V = {s: 0 for s in S}

        while True:
            oldV = V.copy()

            for s in S:
                a = policy[s]
                V[s] = R(s, a) + gamma * sum(P(s_next, s, a) * oldV[s_next] for s_next in S)
            
            if all(oldV[s] == V[s] for s in S):
                break
        
        return V
    
    # https://www.youtube.com/watch?v=RlugupBiC6w
    def policy_improvement(V, S, A, P, R, gamma):
        policy = {s: (0, 0) for s in S}

        for s in S:
            Q = {}

            for a in A(maze, s):
                Q[a] = R(s, a) + gamma * sum(P(s_next, s, a) * V[s_next] for s_next in S)
            
            policy[s] = max(Q, key=Q.get)
        
        return policy

    # https://www.youtube.com/watch?v=RlugupBiC6w
    def policy_iteration(S, A, P, R, gamma=0.9):
        policy = {s: (0, 0) for s in S}

        while True:
            old_policy = policy.copy()

            V = policy_evaluation(policy, S, P, R, gamma)
            policy = policy_improvement(V, S, A, P, R, gamma)

            if all(old_policy[s] == policy[s] for s in S):
                break
        
        return policy
    
    optimal_policy = policy_iteration(S, A, P, R)

    # Get the optimal path
    s = tuple(start)
    path = [s]
    while s != tuple(end):
        a = optimal_policy[s]
        dx, dy = a
        s_next = (s[0] + dx, s[1] + dy)
        path.append(s_next)
        s = s_next

    return path

def print_path(path):
    if path is None:
        print("No path found!")
    else:
        print("Path found:")
        for x, y in path:
            print(f"({x}, {y})")

if __name__ == '__main__':
    grid, start, end = load_maze(MAZE_FILE_PATH)
    path = mdp_policy_iteration(grid, start, end)

    # Create the canvas
    window, canvas = create_canvas()

    # Draw the maze on the canvas
    draw_maze(canvas, grid, start, end, path=path)

    # Start the main tkinter loop
    window.mainloop()