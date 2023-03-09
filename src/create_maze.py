import tkinter as tk
import random
import json

# Set up the grid size and cell size
GRID_SIZE = 25
CELL_SIZE = 20

RES_DIR_PATH = '../res'
MAZE_FILE_PATH = f'{RES_DIR_PATH}/maze.json'

def create_canvas():
    # Create the tkinter window and canvas
    window = tk.Tk()
    canvas = tk.Canvas(window, width=CELL_SIZE*GRID_SIZE, height=CELL_SIZE*GRID_SIZE)
    canvas.pack()
    return window, canvas

def generate_maze(grid_size):
    # Create the grid as a 2D list of cells
    grid = [[{'top': True, 'bottom': True, 'left': True, 'right': True} for _ in range(grid_size)] for _ in range(grid_size)]

    # Set the starting and ending positions
    start = (0, 0)
    end = (grid_size - 1, grid_size - 1)

    # Implement Depth-First Search algorithm to generate random maze
    stack = [start]
    visited = set()

    while stack:
        current = stack.pop()
        visited.add(current)

        # Find all unvisited neighbors
        neighbors = []
        x, y = current
        if x > 0 and (x-1, y) not in visited:
            neighbors.append((x-1, y, 'left', 'right'))
        if y > 0 and (x, y-1) not in visited:
            neighbors.append((x, y-1, 'top', 'bottom'))
        if x < grid_size-1 and (x+1, y) not in visited:
            neighbors.append((x+1, y, 'right', 'left'))
        if y < grid_size-1 and (x, y+1) not in visited:
            neighbors.append((x, y+1, 'bottom', 'top'))

        if neighbors:
            # Choose a random neighbor and remove the wall between them
            neighbor_x, neighbor_y, wall1, wall2 = random.choice(neighbors)
            grid[x][y][wall1] = False
            grid[neighbor_x][neighbor_y][wall2] = False
            stack.append(current)
            stack.append((neighbor_x, neighbor_y))

    return grid, start, end

def draw_maze(canvas, grid, start, end, path=None):
    # Draw the cells and their borders on the canvas
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x1 = i * CELL_SIZE
            y1 = j * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            # Draw the walls of each cell based on the grid
            if grid[i][j]['top']:
                canvas.create_line(x1, y1, x2, y1, width=2)
            if grid[i][j]['bottom']:
                canvas.create_line(x1, y2, x2, y2, width=2)
            if grid[i][j]['left']:
                canvas.create_line(x1, y1, x1, y2, width=2)
            if grid[i][j]['right']:
                canvas.create_line(x2, y1, x2, y2, width=2)

            # Highlight the path if it is given and if the current cell is in the path
            if path and (i, j) in path:
                canvas.create_rectangle(x1, y1, x2, y2, fill='yellow')

    # Mark the start and end positions
    canvas.create_rectangle(CELL_SIZE*start[0], CELL_SIZE*start[1], CELL_SIZE*(start[0]+1), CELL_SIZE*(start[1]+1), fill='green')
    canvas.create_rectangle(CELL_SIZE*end[0], CELL_SIZE*end[1], CELL_SIZE*(end[0]+1), CELL_SIZE*(end[1]+1), fill='red')

def save_maze(grid, start, end, file_path):
    with open(file_path, 'w') as f:
        json.dump({'grid': grid, 'start': start, 'end': end}, f)

def load_maze(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data['grid'], data['start'], data['end']
    
def main():
    # Create the canvas and generate the maze
    window, canvas = create_canvas()
    grid, start, end = generate_maze(GRID_SIZE)

    # Save the maze to a file
    save_maze(grid, start, end, MAZE_FILE_PATH)

    # Load the maze from the file
    grid, start, end = load_maze(MAZE_FILE_PATH)

    # Draw the maze on the canvas
    draw_maze(canvas, grid, start, end)

    # Start the main tkinter loop
    window.mainloop()

if __name__ == '__main__':
    main()