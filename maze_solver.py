#!/usr/bin/env python3
from typing import Optional
from collections import deque


def solve(grid: list, entry: tuple, exit_: tuple) -> Optional[str]:

    height: int = len(grid)
    weidth: int = len(grid[0])
    wall_mask: dict = {"N": 1, "E": 2, "S": 4, "W": 8}
    directions: dict = {
        "N": (0, -1),
        "E": (1,  0),
        "S": (0,  1),
        "W": (-1, 0)
    }

    queue: deque = deque([entry])
    visited: set = {entry}
    came_from: dict = {entry :None}

    while queue:
        x, y = queue.popleft()
        if (x, y) == exit_:
           break
        cell: int = int(grid[y][x], 16) 
        for	direction, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy
            if not ( 0 <= nx < weidth and 0 <= ny < height):
               continue
            if cell & wall_mask[direction] != 0:
               continue
            if (nx, ny) in visited:
                continue
            visited.add((nx,ny))
            came_from[(nx, ny)] = ((x , y), direction)
            queue.append((nx, ny))
        
    if exit_ not in came_from:
        print("ERROR, no path found between wntry and exit")
        return None
    path: list = []
    current: tuple = exit_     
    while came_from.get(current) is not None:
        parent, direction = came_from[current]
        path.append(direction)
        current = parent

    path.reverse()
    return "".join(path)

if __name__ == "__main__":

    grid = [
        "913",   # row 0
        "8A2",   # row 1
        "C46",   # row 2
    ]
    entry = (0,0)
    exit_ = (2,2)
    result = solve(grid, entry, exit_)
    print(result)