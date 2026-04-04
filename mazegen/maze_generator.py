#!/usr/bin/env python3

import random
from typing import Optional


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        seed: None | int = 0,
        perfect: bool = True
    ) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.maze: Optional[list[list[dict[str, bool]]]] = None
        self.path = None
        self.perfect = perfect
        self.pattern_cells: set = set()

    def generate(self) -> None:
        if self.seed is not None:
            random.seed(self.seed)

        self.maze = []
        visited = []

        for y in range(self.height):
            row = []
            visit = []
            for x in range(self.width):
                row.append({"N": True, "E": True, "S": True, "W": True})
                visit.append(False)
            self.maze.append(row)
            visited.append(visit)

        # build pattern cells before generating maze
        self.build_pattern_cells()

        # generate maze
        self.DFS(0, 0, visited)

        if not self.perfect:
            self.imperfect()

        # finally close the pattern cells
        self.pattern_42()

    # 42 PATTERN
    def build_pattern_cells(self) -> None:
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

    def pattern_42(self) -> None:
        if self.maze is None:
            raise ValueError("Maze not generated yet")
        for x, y in self.pattern_cells:
            for d in ("N", "E", "S", "W"):
                self.maze[y][x][d] = True

    # MAZE GENERATION
    def DFS(self, start_x: int, start_y: int, visited: list[list]) -> None:
        if self.maze is None:
            raise ValueError("Maze not generated yet")

        stack = [(start_x, start_y)]

        while stack:

            x, y = stack[-1]
            visited[y][x] = True

            directions = [
                ("N", "S", 0, -1),
                ("S", "N", 0, 1),
                ("E", "W", 1, 0),
                ("W", "E", -1, 0),
            ]

            random.shuffle(directions)

            moved = False

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

                    stack.append((nx, ny))
                    moved = True
                    break

            if not moved:
                stack.pop()

    # IMPERFECT MAZE OPTION

    def check_open_area(self, x: int, y: int) -> bool:
        if self.maze is None:
            raise ValueError("Maze not generated yet")
        for bx in range(x - 2, x + 1):
            for by in range(y - 2, y + 1):

                if bx >= 0 and bx + 2 < self.width and by >= 0 \
                   and by + 2 < self.height:

                    close = False

                    for j in range(3):
                        for i in range(3):

                            if (self.maze[by + j][bx + i]["E"] and i != 2) or (
                                self.maze[by + j][bx + i]["S"] and j != 2
                            ):
                                close = True
                                break

                        if close:
                            break

                    if not close:
                        return True

        return False

    def imperfect(self) -> None:
        if self.maze is None:
            raise ValueError("Maze not generated yet")

        removable_walls = []

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.pattern_cells:
                    continue
                if self.maze[y][x]["E"] and x + 1 < self.width:
                    if (x + 1, y) not in self.pattern_cells:
                        removable_walls.append((y, x, "E"))

                if self.maze[y][x]["S"] and y + 1 < self.height:
                    if (x, y + 1) not in self.pattern_cells:
                        removable_walls.append((y, x, "S"))

        random.shuffle(removable_walls)

        for i in range(self.height * self.width * 10 // 100):

            y_remove, x_remove, direct = removable_walls[i]

            self.maze[y_remove][x_remove][direct] = False

            if direct == "E":
                self.maze[y_remove][x_remove + 1]["W"] = False

            elif direct == "S":
                self.maze[y_remove + 1][x_remove]["N"] = False

            if self.check_open_area(x_remove, y_remove):

                self.maze[y_remove][x_remove][direct] = True

                if direct == "E":
                    self.maze[y_remove][x_remove + 1]["W"] = True

                elif direct == "S":
                    self.maze[y_remove + 1][x_remove]["N"] = True

    # PRINT MAZE

    def print_maze(self) -> None:
        if self.maze is None:
            raise ValueError("Maze not generated yet")

        print("█" + "████" * self.width)

        for y in range(self.height):

            row_mid = ""
            row_bot = ""

            for x in range(self.width):

                row_mid += "█" if self.maze[y][x]["W"] else " "

                if all(self.maze[y][x][d] for d in ("N", "E", "S", "W")):
                    row_mid += "   "
                else:
                    row_mid += "   "

                row_bot += "█"
                row_bot += "███" if self.maze[y][x]["S"] else "   "

            row_mid += "█" if self.maze[y][self.width - 1]["E"] else " "
            row_bot += "█"

            print(row_mid)
            print(row_bot)

    def generate_hex_values(self) -> list[list]:
        if self.maze is None:
            raise ValueError("Maze not generated yet")

        hex_values = []

        N_value = 1
        E_value = 2
        S_value = 4
        W_value = 8

        hex_format = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
        ]
        for y in range(self.height):
            hex_row = []
            for x in range(self.width):
                total = 0
                if self.maze[y][x]["N"] is True:
                    total += N_value
                if self.maze[y][x]["E"] is True:
                    total += E_value
                if self.maze[y][x]["S"] is True:
                    total += S_value
                if self.maze[y][x]["W"] is True:
                    total += W_value
                hex_row.append(hex_format[total])
            hex_values.append(hex_row)
        return hex_values

    def write_output(self, filepath: str, entry: tuple, exit: tuple) -> None:
        if self.maze is None:
            raise ValueError("Maze not generated yet")

        hex_values = self.generate_hex_values()
        with open(filepath, "w") as f:
            for y in range(self.height):
                for x in range(self.width):
                    f.write(hex_values[y][x])
                f.write("\n")
            f.write("\n")
            f.write(str(entry) + "\n")
            f.write(str(exit) + "\n")

    def generate_hex_maze(self) -> None:
        hex_values = self.generate_hex_values()
        f = open("maze.txt", "w")
        for x in range(self.height):
            for y in range(self.width):
                f.write(hex_values[x][y])
            f.write("\n")
        f.close()
        