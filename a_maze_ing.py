#!/usr/bin/env python3

from config_parser import parsing
from maze_display import user_interaction_loop
import sys


if __name__ == "__main__":
    config = parsing("config.txt")
    if config is None:
        sys.exit(0)

    user_interaction_loop(
        width=config["WIDTH"],
        height=config["HEIGHT"],
        seed=config["SEED"],
        perfect=config["PERFECT"],
        entry=config["ENTRY"],
        exit_=config["EXIT"],
    )
