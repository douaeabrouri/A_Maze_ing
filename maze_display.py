#!/usr/bin/env python3

import random
import os
from typing import Optional
from maze_generator import MazeGenerator
from maze_solver import solve

COLORS = [
    "\033[34m",
    "\033[31m",
    "\033[32m",
    "\033[33m",
    "\033[37m",
]
RESET = "\033[0m"
COLOR_NAMES = ["Blue", "Red", "Green", "Yellow", "White"]

def print_maze(
    maze: list,
    width: int,
    height: int,
    entry: tuple = (0, 0),
    exit_: tuple = (-1, -1),
    path_cells: Optional[set] = None,
    show_path: bool = False,
    wall_color: str = "\033[34m"
) -> None:
    """Print the maze visually in the terminal.

    Args:
        maze: 2D list of dicts with N/E/S/W wall states.
        width: maze width.
        height: maze height.
        entry: entry cell coordinates (x, y).
        exit_: exit cell coordinates (x, y).
        path_cells: set of (x,y) tuples on the solution path.
        show_path: if True, display the solution path.
        wall_color: ANSI color code for walls.
    """
    if path_cells is None:
        path_cells = set()

    W = wall_color
    R = RESET

    # top border
    print(f"{W}██{'████' * width}{R}")

    for y in range(height):
        row_mid = ""
        row_bot = ""

        for x in range(width):
            cell = maze[y][x]

            # west wall or passage ← exactly 2 chars
            row_mid += f"{W}██{R}" if cell["W"] else "  "

            # cell content ← exactly 2 chars
            if (x, y) == entry:
                row_mid += "🦋"        # magenta EN
            elif (x, y) == exit_:
                row_mid += "🌺"        # red EX
            elif show_path and (x, y) in path_cells:
                row_mid += "🦋"        # yellow background
            elif all(cell[d] for d in ("N", "E", "S", "W")):
                row_mid += f"{W}▓▓{R}"                # 42 pattern
            else:
                row_mid += "  "                       # empty ← 2 spaces!

            # south wall ← exactly 2 chars
            row_bot += f"{W}██{R}"
            row_bot += f"{W}██{R}" if cell["S"] else "  "  # ══ not ███!

        # east border
        row_mid += f"{W}██{R}"
        row_bot += f"{W}██{R}"

        print(row_mid)
        print(row_bot)
        
def path_to_cells(
    path: Optional[str],
    start: tuple
) -> set:
    """Convert path string like 'EESS' to set of (x,y) cells.
 
    Args:
        path: direction string.
        start: starting cell.
 
    Returns:
        Set of (x, y) tuples on the path.
    """
    cells: set = set()
    if path is None:
        return cells
    x, y = start
    cells.add((x, y))
    moves = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    for d in path:
        dx, dy = moves[d]
        x += dx
        y += dy
        cells.add((x, y))
    return cells

def user_interaction_loop(
    width: int,
    height: int,
    seed: Optional[int],
    perfect: bool,
    entry: tuple,
    exit_: tuple
) -> None:
    """Run the interactive maze display loop.

    Args:
        width: maze width.
        height: maze height.
        seed: random seed (None for random).
        perfect: whether maze is perfect.
        entry: entry cell coordinates.
        exit_: exit cell coordinates.
    """
    color_index: int = 0
    show_path: bool = False
    current_seed = seed
    # generate first maze
    gen = MazeGenerator(width, height, current_seed, perfect)
    gen.generate()
    # solve it
    hex_grid = ["".join(row) for row in gen.generate_hex_values()]
    path_str = solve(hex_grid, entry, exit_)
    path_cells = path_to_cells(path_str, entry)
    while True:
        print_maze(
            maze=gen.maze,
            width=width,
            height=height,
            entry=entry,
            exit_=exit_,
            path_cells=path_cells,
            show_path=show_path,
            wall_color=COLORS[color_index]
        )
        print(f"\n{COLORS[color_index]}=== A-Maze-ing ==={RESET}")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path")
        print(f"3. Change wall color"
              f" (current: {COLORS[color_index]}"
              f"{COLOR_NAMES[color_index]}{RESET})")
        print("4. Quit")
        choice = input("Choice (1-4): ").strip()
        if choice == "1":
            # regenerate with new random seed
            current_seed = random.randint(0, 99999)
            gen = MazeGenerator(width, height, current_seed, perfect)
            gen.generate()
            hex_grid = ["".join(row) for row in gen.generate_hex_values()]
            path_str = solve(hex_grid, entry, exit_)
            path_cells = path_to_cells(path_str, entry)
            show_path = False
        elif choice == "2":
            os.system("clear")
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(COLORS)
        elif choice == "4":
            try:
                with open("butterfly.txt", "r") as f:
                    butterfly = f.read()
                print("\033[35m" + butterfly + "\033[0m")
            except FileNotFoundError:
                print("\033[35m 🦋 \033[0m")
            break
        else:
            print("Invalid choice, please enter 1-4.")
            break
if __name__ == "__main__":
    user_interaction_loop(
        width=16,
        height=16,
        seed=42,
        perfect=True,
        entry=(0, 0),
        exit_=(15, 15)
    )