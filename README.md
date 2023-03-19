# Maze Solver

This project consists of two Python scripts that generate and solve mazes using various algorithms. The `create_maze.py` script creates a maze using the Depth-First Search (DFS) algorithm. The `solve_maze.py` script solve the maze using one of the following algorithms:
1. Depth-First Search (DFS)
2. Breadth-First Search (BFS)
3. A* Search
4. Markov Decision Process (MDP) Value Iteration
5. Markov Decision Process (MDP) Policy Iteration

## Prerequisites

To run this project, you willl need Python 3.6 or later. Additionally, you will need the following Python packages:
- `tkinter`
- `random`
- `json`
- `argparse`
- `collections`
- `heapq`

## Cloning and Running the Project

First clone the repository:
```
git clone https://github.com/hamza-mughees/AI-Assignment1.git
```

### Creating a Maze

To create a maze, navigate to the `src` directory and run the `create_maze.py` script with the desired grid size and cell size:
```
python create_maze.py --grid <grid size> --cell <cell size>
```
This command will generate a maze with the provided grid size and cell size configuration and save it as `maze.json` in the res directory. The script will also create a `config.json` file in the same directory, which contains the configuration of the maze.

### Solving a Maze

To solve the maze, run the `solve_maze.py` script with the desired algorithm:
```
python solve_maze.py --algorithm <algorithm>
```
Replace `<algorithm>` with one of the following oprtions:
- `dfs` for DFS
- `bfs` for BFS
- `a_star` for A* Search
- `mdp_value` for MDP Value Iteration
- `mdp_policy` for MDP Policy Iteration

For example, if you want to use the A* Search algorithm, run:
```
python solve_maze.py --algorithm a_star
```
After executing the script, you will see the time complexity and the number of nodes visited or iterations taken, depending on the algorithm. A Tkinter window will display the maze and the solution path.