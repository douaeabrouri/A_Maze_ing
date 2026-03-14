#!/usr/bin/env python3

def validate_walls(grid: list) -> bool:
    height: int = len(grid)
    widght: int = len(grid[0])

    for y in range(height):
            for x in range(widght):
                cell: int = int(grid[y][x], 16)
                if x + 1 < widght:
                   right: int = int(grid[y][x+1], 16)
                   has_east: int = cell & 2
                   has_west: int = right & 8
                if bool(has_east) != bool(has_west):
                        print(f"Error: wall mismatch at ({x},{y}) East"
                              f" vs ({x+1},{y}) West")
                        return False
                if y + 1 < height:
                    below: int = int(grid[y+1][x], 16)
                    has_north: int = cell & 1
                    has_south: int = below & 4
                    if bool(has_north) != bool(has_south):
                        print(f"Error: wall mismatch at ({x},{y}) East"
                            f" vs ({x},{y + 1}) West")
                        return False
            return True
