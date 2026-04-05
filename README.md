*This project has been created as part of the 42 curriculum by doabrour, yhamdaou.*

# A-Maze-ing 🦋🌺

## Description

A-Maze-ing is a Python maze generator and visualizer built as part of the 42 curriculum. The program generates mazes using the **Depth-First Search (DFS)** algorithm, displays them visually in the terminal with an underwater theme 🌊, and finds the shortest path from the entrance to the exit using **BFS (Breadth-First Search)**.

The maze can be either **perfect** (one unique path between any two points) or **imperfect** (multiple paths). It also features a hidden **"42" pattern** embedded inside every maze as a tribute to the school.

---

## Instructions

### Requirements

- Python 3.10 or later
- pip

### Installation

```bash
make install
```

### Run

```bash
make run
```

Or directly:

```bash
python3 a_maze_ing.py config.txt
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint
```

### Clean

```bash
make clean
```

---

## Config File

The configuration file must contain one `KEY=VALUE` pair per line. Lines starting with `#` are comments and are ignored.

### Format

```
# A-Maze-ing configuration file

WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Keys

| Key | Description | Type | Required |
|---|---|---|---|
| `WIDTH` | Number of columns | positive int | ✅ |
| `HEIGHT` | Number of rows | positive int | ✅ |
| `ENTRY` | Start cell as `x,y` | tuple | ✅ |
| `EXIT` | End cell as `x,y` | tuple | ✅ |
| `OUTPUT_FILE` | Output filename | string | ✅ |
| `PERFECT` | Perfect maze? | `True`/`False` | ✅ |

---

## Maze Generation Algorithm

We used the **Depth-First Search (DFS)** algorithm with an iterative stack implementation.

### How it works

1. Start at cell `(0, 0)`
2. Mark it as visited
3. Pick a random unvisited neighbor
4. Remove the wall between current cell and neighbor
5. Move to the neighbor and repeat
6. If no unvisited neighbors → backtrack using the stack
7. Repeat until all cells are visited

### Why DFS?

We chose DFS because it is **easy to implement**, produces mazes with long winding corridors, and naturally generates **perfect mazes** (no loops, one unique path between any two points). It is also well documented and easy to debug.

---

## Visual Display

The maze is displayed in the terminal using block characters with an **underwater theme**:

| Element | Display | Meaning |
|---|---|---|
| `██` | colored blocks | walls |
| `🦋` | magenta | entry cell |
| `🌺` | red | exit cell |
| yellow background | `  ` | solution path |
| `▓▓` | colored | 42 pattern cells |

### User Interactions

| Key | Action |
|---|---|
| `1` | Re-generate a new maze |
| `2` | Show/Hide shortest path |
| `3` | Cycle wall colors |
| `4` | Quit with butterfly 🦋 |

### Available Wall Colors

- 🔵 Blue (default)
- 🔴 Red
- 🟢 Green
- 🟡 Yellow
- ⚪ White
- 🟣 Purple `\033[38;2;229;208;255m`

---

## Reusable Code

The maze generation logic is implemented as a standalone class `MazeGenerator` inside `maze_generator.py`. It can be installed as a pip package (`mazegen-*.whl`) and reused in any future project.

### How to use it

```python
from maze_generator import MazeGenerator

# create a generator
gen = MazeGenerator(
    width=20,
    height=15,
    perfect=True    # True = perfect maze, False = imperfect
)

# generate the maze
gen.generate()

# access the maze structure (2D list of dicts)
maze = gen.maze
# maze[y][x] = {"N": True, "E": False, "S": True, "W": False}
# True = wall exists, False = wall open

# get hex grid format for solver/validator
hex_grid = ["".join(row) for row in gen.generate_hex_values()]

# print the maze
gen.print_maze(
    entry=(0, 0),
    exit_=(19, 14),
    show_path=False,
    wall_color="\033[34m"
)
```

### Custom parameters

| Parameter | Type | Description |
|---|---|---|
| `width` | int | number of columns |
| `height` | int | number of rows |
| `perfect` | bool | perfect or imperfect maze |

### Install as pip package

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

---

## Team and Project Management

### Roles

| Member | Role |
|---|---|
| `yhamdaou` | Maze generation (DFS algorithm,  42 pattern, imperfect maze, hex output) |
| `doabrour` | Solving (BFS shortest path), validation (wall coherence), display (ASCII terminal render, user interactions, colors), config parser, main wiring, Makefile, README |

### Planning

**Initial plan:**
- Week 1: understand the subject, split tasks, set up repo
- Week 2: maze generation + config parser + validator
- Week 3: BFS solver + display + user interactions
- Week 4: main wiring + packaging + README + testing

**How it evolved:**
- The display took more time than expected due to emoji alignment issues
- We had to coordinate on the maze data format (dict vs hex) between generation and solving
- The 42 pattern required extra care to not be broken by the imperfect maze option

### What worked well

- Clear task separation between team members
- Using a shared format (hex grid) between all modules
- Testing each module independently before wiring everything together

### What could be improved

- Better communication on data formats from the start
- More unit tests to catch bugs earlier
- Could have used GitHub issues to track tasks

### Tools used

- **VSCode** — code editor
- **GitHub** — version control and collaboration
- **Claude AI** — used for understanding concepts (BFS, bit masking, ANSI colors), debugging errors, and getting explanations on Python typing and flake8 rules

---

## Resources

### Maze generation
- [Maze generation algorithms - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Depth-First Search explanation](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [Jamis Buck's Maze algorithms](http://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)

### BFS pathfinding
- [BFS - Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Red Blob Games - BFS](https://www.redblobgames.com/pathfinding/a-star/introduction.html)

### Python
- [Python typing module](https://docs.python.org/3/library/typing.html)
- [flake8 documentation](https://flake8.pycqa.org/en/latest/)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [Python collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)

### ASCII art
- [ASCII art butterflies](https://www.asciiart.eu/animals/insects/butterflies)

### AI usage
- **Claude AI** was used for:
  - Explaining BFS and DFS algorithms
  - Understanding bit masking for hex wall encoding
  - Understanding ANSI color codes for terminal display
  - Reviewing and correcting code logic
