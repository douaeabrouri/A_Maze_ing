from config_parser import parsing
from maze_generator import MazeGenerator

config = parsing("config.txt")

if config:

    gen = MazeGenerator(
        width=config["WIDTH"],
        height=config["HEIGHT"],
        seed=config["SEED"],
        perfect=config["PERFECT"]
    )
    gen.generate()
    gen.print_maze()
    gen.write_output(config["OUTPUT_FILE"], config["ENTRY"], config["EXIT"])
