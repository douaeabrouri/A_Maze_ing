#!/usr/bin/env python3
import random
from typing import Optional
import tty
import termios
import sys
# import time

class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        perfect: bool = True
    ) -> None:
        self.width = width
        self.height = height
        self.maze: Optional[list[list[dict[str, bool]]]] = None
        self.path = None
        self.perfect = perfect
        self.pattern_cells: set = set()

    def generate(self) -> None:
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
        self.build_pattern_cells()
        self.DFS(0, 0, visited)
        if not self.perfect:
            self.imperfect()
        self.pattern_42()

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

    def generate_hex_maze(self) -> None:
        hex_values = self.generate_hex_values()
        with open("maze.txt", "w") as f:
            for x in range(self.height):
                for y in range(self.width):
                    f.write(hex_values[x][y])
                f.write("\n")
    def get_key(self) -> str:
        """Read a single keypress without Enter.
    
        Returns:
            The key pressed as a string.
        """
        import select
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\033":
                # wait max 0.05 seconds for more chars
                ready = select.select([sys.stdin], [], [], 0.05)[0]
                if ready:
                    ch2 = sys.stdin.read(1)
                    ready = select.select([sys.stdin], [], [], 0.05)[0]
                    if ready:
                        ch3 = sys.stdin.read(1)
                        return ch + ch2 + ch3
                    return ch + ch2
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    def play(self, entry: tuple, exit_: tuple) -> None:
        """Play the maze game.
    
        Args:
            entry: starting cell.
            exit_: target cell.
        """
        import os
        from maze_display import print_maze
    
        player = entry
        message = ""
    
        while player != exit_:
            os.system("clear")
    
            print_maze(
                maze=self.maze,
                width=self.width,
                height=self.height,
                entry=entry,
                exit_=exit_,
                player=player
            )
    
            print(f"\n  Player: {player}")
            print("  Move with ↑←↓→ or WASD | Q to quit")
            if message:
                print(f"  \033[31m{message}\033[0m")
    
            key = self.get_key()
    
            if key in ("q", "Q"):
                break
    
            x, y = player
            message = ""

            if key in ("w", "W", "\033[A") and not self.maze[y][x]["N"]:
               player = (x, y - 1)
            elif key in ("s", "S", "\033[B") and not self.maze[y][x]["S"]:
                player = (x, y + 1)
            elif key in ("d", "D", "\033[C") and not self.maze[y][x]["E"]:
                player = (x + 1, y)
            elif key in ("a", "A", "\033[D") and not self.maze[y][x]["W"]:
                player = (x - 1, y)
            else:
                message = "Can't move that way!"
    
        if player == exit_:
            os.system("clear")
            print("\033[32m\n  🎉 You win! 🎉\033[0m")
