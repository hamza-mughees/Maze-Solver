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

def print_path(path):
    if path is None:
        print("No path found!")
    else:
        print("Path found:")
        for x, y in path:
            print(f"({x}, {y})")

if __name__ == '__main__':
    grid, start, end = load_maze(MAZE_FILE_PATH)
    path = a_star(grid, start, end)

    # Create the canvas
    window, canvas = create_canvas()

    # Draw the maze on the canvas
    draw_maze(canvas, grid, start, end, path=path)

    # Start the main tkinter loop
    window.mainloop()