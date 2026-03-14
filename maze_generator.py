import random

class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int = None, perfect: bool = True) -> None:
        self.width = width          # Number of columns in the maze
        self.height = height        # Number of rows in the maze
        self.seed = seed            # Optional seed to make random generation reproducible
        self.maze = None            # Will store the maze structure
        self.path = None            # Placeholder for storing a path (not used yet)

    # Main method that generates the maze
    def generate(self) -> None:

        # If a seed is provided, initialize the random generator with it
        # This ensures the same maze can be reproduced
        if self.seed is not None:
            random.seed(self.seed)

        # Initialize the maze grid and visited grid
        self.maze = []
        visited = []

        # Create the grid structure
        for y in range(self.height):
            row = []     # Represents a row of cells in the maze
            visit = []   # Keeps track of visited cells for DFS

            for x in range(self.width):
                # Each cell starts with all four walls present
                row.append({"N": True, "E": True, "S": True, "W": True})

                # Initially no cell has been visited
                visit.append(False)

            self.maze.append(row)
            visited.append(visit)

        # Start generating the maze using Depth First Search from cell (0,0)
        self.DFS(0, 0, visited)

        # If the maze should NOT be perfect (i.e., allow loops)
        if self.perfect == False:
            self.imperfect
<<<<<<< HEAD
 
=======


    # Creates an imperfect maze by removing additional random walls
    # This introduces loops instead of a single unique path
>>>>>>> 87d8e25c9ec6020c5ace258c092a640fa34cf133
    def imperfect(self):

        removable_walls = []

        # Collect all walls that could potentially be removed
        for y in range(self.height):
            for x in range(self.width):

                # East wall can be removed if there is a cell to the right
                if self.maze[y][x]["E"] == True and x + 1 < self.width:
                    removable_walls.append((y, x, "E"))

                # South wall can be removed if there is a cell below
                elif self.maze[y][x]["S"] == True and y + 1 < self.height:
                    removable_walls.append((y, x, "S"))

        # Shuffle walls so removals are random
        random.shuffle(removable_walls)

        # Remove around 10% of possible walls
        for i in range(self.height * self.width * 10 // 100):

            y_remove = removable_walls[i][0]
            x_remove = removable_walls[i][1]
            direct = removable_walls[i][2]

            # Remove the wall in the current cell
            self.maze[y_remove][x_remove][direct] = False

            # Remove the corresponding wall in the neighboring cell
            if direct == "E":
                self.maze[y_remove][x_remove + 1]["W"] = False

            if direct == "S":
                self.maze[y_remove + 1][x_remove]["N"] = False


    # Depth First Search algorithm used to carve the maze
    # It recursively visits cells and removes walls between them
    def DFS(self, x: int, y: int, visited: list[list]) -> None:

        # List of possible directions:
        # (current_wall, opposite_wall, dx, dy)
        directions = [
            ("N", "S", 0, -1),
            ("S", "N", 0, 1),
            ("E", "W", 1, 0),
            ("W", "E", -1, 0)
        ]

        # Mark the current cell as visited
        visited[y][x] = True

        # Shuffle directions to make the maze random
        random.shuffle(directions)

        # Try all four directions
        for i in range(4):

            # Compute coordinates of neighboring cell
            nx = x + directions[i][2]
            ny = y + directions[i][3]

            # Check if neighbor is inside the grid and not visited yet
            if nx >= 0 and nx < self.width and ny >= 0 and ny < self.height and visited[ny][nx] == False:

                # Remove wall between current cell and neighbor
                self.maze[y][x][directions[i][0]] = False

                # Remove opposite wall in the neighbor cell
                self.maze[ny][nx][directions[i][1]] = False
<<<<<<< HEAD
=======

                # Recursively continue DFS from the neighbor
>>>>>>> 87d8e25c9ec6020c5ace258c092a640fa34cf133
                self.DFS(nx, ny, visited)
