#!/usr/bin/env python3

from config_parser import parsing
from maze_display import user_interaction_loop
from maze_solver import solve
import sys


if __name__ == "__main__":
    config = parsing("config.txt")
    if config is None:
       sys.exit(0)

    gen = user_interaction_loop(
        width=config["WIDTH"],
        height=config["HEIGHT"],
        # seed=config["SEED"],
        perfect=config["PERFECT"],
        entry=config["ENTRY"],
        exit_=config["EXIT"],
    )
    gen.generate_hex_maze()
    f = open("maze.txt", "a")
    f.write("\n")
    f.write(f"{config['ENTRY'][0]}, {config['ENTRY'][1]}\n")
    f.write(f"{config['EXIT'][0]}, {config['EXIT'][1]}\n")

    hex_grid = ["".join(row) for row in gen.generate_hex_values()]

    path = solve(hex_grid, config["ENTRY"], config["EXIT"])
    f.write(path)
