# row = [{"N": True}] * 5
# row[0]["N"] = False
# print(row)

# def add_to_list(item, my_list=[]):
#   my_list.append(item)
#   return my_list

# print(add_to_list(1))
# print(add_to_list(2))


# def add_to_list_safe(item, my_list=None):
#   # If no list was given, create a brand new one.
#   if my_list is None:
#     my_list = []

#   my_list.append(item)
#   return my_list

# print(add_to_list_safe(1))
# print(add_to_list_safe(2))





def DFS(self, start_x: int, start_y: int, visited: list[list]) -> None:

    stack = [(start_x, start_y)]

    while stack:

        x, y = stack[-1]
        visited[y][x] = True

        directions = [
            ("N", "S", 0, -1),
            ("S", "N", 0, 1),
            ("E", "W", 1, 0),
            ("W", "E", -1, 0)
        ]

        random.shuffle(directions)

        moved = False

        for d, opposite, dx, dy in directions:

            nx = x + dx
            ny = y + dy

            if (
                0 <= nx < self.width
                and 0 <= ny < self.height
                and not visited[ny][nx]
                and (nx, ny) not in self.pattern_cells
            ):

                self.maze[y][x][d] = False
                self.maze[ny][nx][opposite] = False

                stack.append((nx, ny))
                moved = True
                break

        if not moved:
            stack.pop()
