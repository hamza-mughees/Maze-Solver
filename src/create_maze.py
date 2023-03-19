import tkinter as tk
import random
import json
import sys
import argparse

RES_DIR_PATH = '../res'
MAZE_FILE_PATH = f'{RES_DIR_PATH}/maze.json'
CONFIG_FILE_PATH = f'{RES_DIR_PATH}/config.json'

def save_config(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)

def create_canvas(cell_size, grid_size):
    # Create the tkinter window and canvas
    window = tk.Tk()
    canvas = tk.Canvas(window, width=cell_size*grid_size, height=cell_size*grid_size)
    canvas.pack()
    return window, canvas

def generate_maze(cell_size, grid_size):
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

def draw_maze(canvas, cell_size, grid_size, grid, start, end, path=None):
    # Draw the cells and their borders on the canvas
    for i in range(grid_size):
        for j in range(grid_size):
            x1 = i * cell_size
            y1 = j * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

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
                canvas.create_rectangle(x1, y1, x2, y2, fill='yellow', outline='')

    # Mark the start and end positions
    MARGIN_SIZE = (1/4)*cell_size
    canvas.create_rectangle(
        cell_size*start[0] + MARGIN_SIZE,
        cell_size*start[1] + MARGIN_SIZE,
        cell_size*(start[0]+1) - MARGIN_SIZE,
        cell_size*(start[1]+1) - MARGIN_SIZE,
        fill='green', outline=''
    )
    canvas.create_rectangle(
        cell_size*end[0] + MARGIN_SIZE,
        cell_size*end[1] + MARGIN_SIZE,
        cell_size*(end[0]+1) - MARGIN_SIZE,
        cell_size*(end[1]+1) - MARGIN_SIZE,
        fill='red', outline=''
    )

def save_maze(grid, start, end, file_path):
    with open(file_path, 'w') as f:
        json.dump({'grid': grid, 'start': start, 'end': end}, f)

def load_maze(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data['grid'], data['start'], data['end']
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--grid', type=int, help='Select the grid size')
    parser.add_argument('--cell', type=int, help='Select the cell size')
    args = parser.parse_args()

    grid_size = args.grid
    cell_size = args.cell

    # Update the configuration file with the new grid size and cell size values
    config_data = {
        "grid_size": grid_size,
        "cell_size": cell_size
    }
    save_config(config_data, CONFIG_FILE_PATH)

    # Create the canvas and generate the maze
    window, canvas = create_canvas(cell_size, grid_size)
    grid, start, end = generate_maze(cell_size, grid_size)

    # Save the maze to a file
    save_maze(grid, start, end, MAZE_FILE_PATH)

    # Load the maze from the file
    grid, start, end = load_maze(MAZE_FILE_PATH)

    # Draw the maze on the canvas
    draw_maze(canvas, cell_size, grid_size, grid, start, end)

    # Start the main tkinter loop
    window.mainloop()

if __name__ == '__main__':
    main()