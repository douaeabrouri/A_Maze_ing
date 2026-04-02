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
    print(f"{W}██{'████' * width}██{R}")

    for y in range(height):
        row_mid = ""
        row_bot = ""

        for x in range(width):
            cell = maze[y][x]

            # west wall or passage ← exactly 2 chars
            row_mid += f"{W}██{R}" if cell["W"] else "  "

            # cell content ← exactly 2 chars
            if (x, y) == entry:
                row_mid += "\033[35mEN\033[0m"        # magenta EN
            elif (x, y) == exit_:
                row_mid += "\033[31mEX\033[0m"        # red EX
            elif show_path and (x, y) in path_cells:
                row_mid += "\033[43m  \033[0m"        # yellow background
            elif all(cell[d] for d in ("N", "E", "S", "W")):
                row_mid += f"{W}▓▓{R}"                # 42 pattern
            else:
                row_mid += "  "                       # empty ← 2 spaces!

            # south wall ← exactly 2 chars
            row_bot += f"{W}██{R}"
            row_bot += f"{W}══{R}" if cell["S"] else "  "  # ══ not ███!

        # east border
        row_mid += f"{W}██{R}"
        row_bot += f"{W}██{R}"

        print(row_mid)
        print(row_bot)