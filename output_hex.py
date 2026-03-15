def generate_hex_values(self):
    hex_values = []

    N_value = 1
    E_value = 2
    S_value = 4
    W_value = 8

    hex_format = [ "0", "1", "2", "3", "4",
        "5","6","7","8","9","A","B","C","D","E","F"
    ]
    for y in range(self.height):
        hex_row = []
        for x in range(self.width):
            total = 0
            if self.maze[y][x]["N"] == True:
                total += N_value
            if self.maze[y][x]["E"] == True:
                total += E_value
            if self.maze[y][x]["S"] == True:
                total += S_value
            if self.maze[y][x]["W"] == True:
                total += W_value
            hex_row.append(hex_format[total])
        hex_values.append(hex_row)

    def write_output(self):
        self.generate_hex_values()
        f = open("output.txt", "w")
        for y in range(self.height):
            for x in range(self.width):
                f.write(hex_values[y][x])
            f.write("\n")