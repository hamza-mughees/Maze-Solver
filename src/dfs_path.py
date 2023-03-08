import json

from create_maze import create_canvas, draw_maze

RES_DIR_PATH = '../res'
MAZE_FILE_PATH = f'{RES_DIR_PATH}/maze.json'

def load_maze(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data['grid'], data['start'], data['end']

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

def get_unvisited_neighbors(maze, x, y):
    neighbors = []
    for dx, dy, wall1, wall2 in [(-1, 0, 'left', 'right'), (0, -1, 'top', 'bottom'), (1, 0, 'right', 'left'), (0, 1, 'bottom', 'top')]:
        if maze[x][y][wall1] == False:
            if 0 <= x + dx < len(maze) and 0 <= y + dy < len(maze) and maze[x+dx][y+dy][wall2] == False:
                neighbors.append((x + dx, y + dy, wall1, wall2))
    return neighbors

def print_path(path):
    if path is None:
        print("No path found!")
    else:
        print("Path found:")
        for x, y in path:
            print(f"({x}, {y})")

if __name__ == '__main__':
    grid, start, end = load_maze(MAZE_FILE_PATH)
    path = depth_first_search(grid, start, end)

    # Create the canvas
    window, canvas = create_canvas()

    # Draw the maze on the canvas
    draw_maze(canvas, grid, start, end, path=path)

    # Start the main tkinter loop
    window.mainloop()