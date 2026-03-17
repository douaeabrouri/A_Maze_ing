#!/usr/bin/env python3

import random
from typing import Optional
from solver import solve


# ─── ANSI Colors ────────────────────────────────────────────
COLORS = [
    "\033[34m",   # blue   (default)
    "\033[31m",   # red
    "\033[32m",   # green
    "\033[33m",   # yellow
    "\033[37m",   # white
]
RESET = "\033[0m"
COLOR_NAMES = ["Blue", "Red", "Green", "Yellow", "White"]


class MazeGenerator:
    """Generates a maze using DFS algorithm.

    Attributes:
        width: number of columns.
        height: number of rows.
        seed: random seed for reproducibility.
        perfect: if True, generates a perfect maze.
        maze: 2D list of dicts with wall states.
        pattern_cells: set of cells used for the 42 pattern.
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
        perfect: bool = True
    ) -> None:
        """Initialize the maze generator.

        Args:
            width: number of columns.
            height: number of rows.
            seed: random seed for reproducibility.
            perfect: if True, generates a perfect maze.
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.maze: list = []
        self.pattern_cells: set = set()

    def generate(self) -> list:
        """Generate the maze and return it as a 2D list of dicts.

        Returns:
            2D list where each cell is a dict with N/E/S/W wall states.
        """
        if self.seed is not None:
            random.seed(self.seed)

        # initialize maze with all walls closed
        self.maze = []
        visited: list = []

        for y in range(self.height):
            row = []
            visit = []
            for x in range(self.width):
                row.append({"N": True, "E": True, "S": True, "W": True})
                visit.append(False)
            self.maze.append(row)
            visited.append(visit)

        # build 42 pattern before generating
        self.build_pattern_cells()

        # generate maze with DFS
        self.dfs(0, 0, visited)

        # add loops if imperfect
        if not self.perfect:
            self.imperfect()

        # close pattern cells (42 shape)
        self.pattern_42()

        return self.maze

    def to_hex_grid(self) -> list:
        """Convert maze dict format to hex string grid format.

        Returns:
            List of strings where each char is a hex digit encoding walls.
        """
        grid: list = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                val = 0
                if self.maze[y][x]["N"]:
                    val += 1   # bit0 = North
                if self.maze[y][x]["E"]:
                    val += 2   # bit1 = East
                if self.maze[y][x]["S"]:
                    val += 4   # bit2 = South
                if self.maze[y][x]["W"]:
                    val += 8   # bit3 = West
                row += format(val, 'x').upper()
            grid.append(row)
        return grid

    # ─── 42 PATTERN ─────────────────────────────────────────

    def build_pattern_cells(self) -> None:
        """Build the set of cells that form the '42' pattern."""
        if self.width >= 12 and self.height >= 9:
            cx = self.width // 2
            cy = self.height // 2

            def add_vertical(x: int, y: int) -> None:
                for i in range(3):
                    self.pattern_cells.add((x, y + i))

            def add_horizontal(x: int, y: int) -> None:
                for i in range(3):
                    self.pattern_cells.add((x + i, y))

            add_vertical(cx - 3, cy - 2)
            add_vertical(cx - 1, cy)
            add_vertical(cx + 1, cy)
            add_vertical(cx + 3, cy - 2)

            add_horizontal(cx - 3, cy)
            add_horizontal(cx + 1, cy - 2)
            add_horizontal(cx + 1, cy)
            add_horizontal(cx + 1, cy + 2)
        else:
            print("Warning: maze too small to display '42' pattern.")

    def pattern_42(self) -> None:
        """Close all walls of pattern cells to make them solid."""
        for (x, y) in self.pattern_cells:
            for d in ("N", "E", "S", "W"):
                self.maze[y][x][d] = True

    # ─── MAZE GENERATION ────────────────────────────────────

    def dfs(self, x: int, y: int, visited: list) -> None:
        """Recursively generate maze using Depth First Search.

        Args:
            x: current cell column.
            y: current cell row.
            visited: 2D list tracking visited cells.
        """
        if (x, y) in self.pattern_cells:
            return

        directions = [
            ("N", "S", 0, -1),
            ("S", "N", 0, 1),
            ("E", "W", 1, 0),
            ("W", "E", -1, 0)
        ]

        visited[y][x] = True
        random.shuffle(directions)

        for d, opposite, dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if (
                0 <= nx < self.width
                and 0 <= ny < self.height
                and not visited[ny][nx]
                and (nx, ny) not in self.pattern_cells
            ):
                self.maze[y][x][d] = False
                self.maze[ny][nx][opposite] = False
                self.dfs(nx, ny, visited)

    # ─── IMPERFECT MAZE ─────────────────────────────────────

    def check_open_area(self, x: int, y: int) -> bool:
        """Check if removing a wall would create a 3x3 open area.

        Args:
            x: cell column.
            y: cell row.

        Returns:
            True if open area would be created, False otherwise.
        """
        for bx in range(x - 2, x + 1):
            for by in range(y - 2, y + 1):
                if (
                    bx >= 0
                    and bx + 2 < self.width
                    and by >= 0
                    and by + 2 < self.height
                ):
                    close = False
                    for j in range(3):
                        for i in range(3):
                            if (
                                (self.maze[by + j][bx + i]["E"] and i != 2)
                                or (self.maze[by + j][bx + i]["S"] and j != 2)
                            ):
                                close = True
                                break
                        if close:
                            break
                    if not close:
                        return True
        return False

    def imperfect(self) -> None:
        """Add random loops to make the maze imperfect."""
        removable_walls: list = []

        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x]["E"] and x + 1 < self.width:
                    removable_walls.append((y, x, "E"))
                if self.maze[y][x]["S"] and y + 1 < self.height:
                    removable_walls.append((y, x, "S"))

        random.shuffle(removable_walls)

        for i in range(self.height * self.width * 10 // 100):
            y_r, x_r, direct = removable_walls[i]
            self.maze[y_r][x_r][direct] = False

            if direct == "E":
                self.maze[y_r][x_r + 1]["W"] = False
            elif direct == "S":
                self.maze[y_r + 1][x_r]["N"] = False

            if self.check_open_area(x_r, y_r):
                self.maze[y_r][x_r][direct] = True
                if direct == "E":
                    self.maze[y_r][x_r + 1]["W"] = True
                elif direct == "S":
                    self.maze[y_r + 1][x_r]["N"] = True

    # ─── DISPLAY ────────────────────────────────────────────

    def print_maze(
        self,
        entry: tuple = (0, 0),
        exit_: tuple = (-1, -1),
        path_cells: Optional[set] = None,
        show_path: bool = False,
        wall_color: str = "\033[34m"
    ) -> None:
        """Print the maze visually in the terminal.

        Args:
            entry: entry cell coordinates (x, y).
            exit_: exit cell coordinates (x, y).
            path_cells: set of (x,y) tuples on the solution path.
            show_path: if True, display the solution path.
            wall_color: ANSI color code for walls.
        """
        if path_cells is None:
            path_cells = set()

        W = wall_color    # wall color
        R = RESET         # reset color

        # top border
        print(f"{W}🌊{'🌊🌊🌊🌊' * self.width}{R}")

        for y in range(self.height):
            row_mid = ""
            row_bot = ""

            for x in range(self.width):
                cell = self.maze[y][x]

                # west wall
                row_mid += f"{W}🌊{R}" if cell["W"] else " "

                # cell content
                if (x, y) == entry:
                    row_mid += "🧜🏼‍♀️"        # entry
                elif (x, y) == exit_:
                    row_mid += "🐠 "         # exit
                elif show_path and (x, y) in path_cells:
                    row_mid += "💎 "         # path
                elif all(cell[d] for d in ("N", "E", "S", "W")):
                    row_mid += "🐙 "         # 42 pattern cell
                else:
                    row_mid += "   "         # empty corridor

                # bottom wall
                row_bot += f"{W}🌊{R}"
                row_bot += f"{W}🌊🌊🌊{R}" if cell["S"] else "   "

            # east border
            row_mid += f"{W}🌊{R}"
            row_bot += f"{W}🌊{R}"

            print(row_mid)
            print(row_bot)


# ─── USER INTERACTION LOOP ──────────────────────────────────

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
    from solver import solve

    color_index: int = 0
    show_path: bool = False
    current_seed = seed

    # generate first maze
    gen = MazeGenerator(width, height, current_seed, perfect)
    gen.generate()

    # solve it
    hex_grid = gen.to_hex_grid()
    path_str = solve(hex_grid, entry, exit_)

    # convert path string to set of cells for display
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

    path_cells = path_to_cells(path_str, entry)

    while True:
        # clear screen
        print("\033[2J\033[H", end="")

        # print maze
        gen.print_maze(
            entry=entry,
            exit_=exit_,
            path_cells=path_cells,
            show_path=show_path,
            wall_color=COLORS[color_index]
        )

        # print menu
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path")
        print(f"3. Change wall color (current: {COLOR_NAMES[color_index]})")
        print("4. Quit")

        choice = input("Choice (1-4): ").strip()

        if choice == "1":
            # regenerate with new random seed
            current_seed = random.randint(0, 99999)
            gen = MazeGenerator(width, height, current_seed, perfect)
            gen.generate()
            hex_grid = gen.to_hex_grid()
            path_str = solve(hex_grid, entry, exit_)
            path_cells = path_to_cells(path_str, entry)
            show_path = False

        elif choice == "2":
            show_path = not show_path   # toggle show/hide

        elif choice == "3":
            # cycle to next color
            color_index = (color_index + 1) % len(COLORS)

        elif choice == "4":
            print("Bye! 🌊")
            break

        else:
            print("Invalid choice, please enter 1-4.")


# ─── TEST ────────────────────────────────────────────────────

if __name__ == "__main__":
    user_interaction_loop(
        width=16,
        height=16,
        seed=42,
        perfect=True,
        entry=(0, 0),
        exit_=(15, 15)
    )