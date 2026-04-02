from config_parser import parsing
from maze_generator import MazeGenerator
from maze_solver import solve
from maze_display import user_interaction_loop
import sys

config = parsing("config.txt")
if config is None:
	sys.exit(1)

user_interaction_loop(
    width=config["WIDTH"],
    height=config["HEIGHT"],
    seed=config["SEED"],
    perfect=config["PERFECT"],
    entry=config["ENTRY"],
    exit_=config["EXIT"]
)