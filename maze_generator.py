import random

class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int = None, perfect:bool = True) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.maze = None
        self.path = None

    def generate(self) -> None:
        if self.seed is not None:
            random.seed(self.seed)
        self.maze = []
        visited = []
        for y in range(self.height):
            row = []
            visit = []
            for x in range(self.width):
                row.append({"N": True, "E": True, "S":True, "W": True})
                visit.append(False)
            self.maze.append(row)
            visited.append(visit)
        self.DFS(0, 0, visited)

        if self.perfect == False:
            self.imperfect
            
    def imperfect(self):
            removable_walls = []
            for y in range(self.height):
                for x in range (self.width):
                    if self.maze[y][x]["E"] == True and x + 1 < self.width:
                        removable_walls.append((y, x, "E"))
                    elif self.maze[y][x]["S"] == True and y + 1 < self.height:
                        removable_walls.append((y, x, "S"))
            random.shuffle(removable_walls)
            for i in range(self.height * self.width * 10 // 100):
                y_remove = removable_walls[i][0]
                x_remove = removable_walls[i][1]
                direct = removable_walls[i][2]
                self.maze[y_remove][x_remove][direct] = False
                if direct == "E":
                    self.maze[y_remove][x_remove - 1]["W"] = False
                if direct == "S":
                    self.maze[y_remove - 1][x_remove]["N"] = False


    def DFS(self, x: int, y: int, visited: list[list]) -> None:
        directions = [
            ("N", "S", 0, -1),
            ("S", "N", 0, 1),
            ("E", "W", 1, 0),
            ("W", "E", -1, 0)
        ]
        visited[y][x] = True
        random.shuffle(directions)
        for i in range(4):
            nx = x + directions[i][2]
            ny = y + directions[i][3]
            if nx >= 0 and nx < self.width and ny >= 0 and ny < self.height and visited[ny][nx] == False:
                self.maze[y][x][directions[i][0]] = False
                self.maze[ny][nx][directions[i][1]] = False
                self.DFS(nx, ny, visited)