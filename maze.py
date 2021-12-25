import random as rnd

from cell import Cell, remove_walls


class Maze:
    def __init__(self, size: int):
        if not size % 2 or size < 5:
            raise ValueError(f"In order for the maze pattern to be symmetrical and readable, "
                             f"the size must be odd and at least 5. Given size: {size}")
        self.total_grid_size = size
        self.cell_row_size = size // 2
        self.cells = [
            [Cell(x, y) for x in range(self.cell_row_size)] for y in range(self.cell_row_size)
        ]

    def get_neighbours(self, cell: Cell) -> list[Cell]:
        return list(filter(lambda c: c and not c.visited, [
            self.get_cell(cell.x,     cell.y - 1),
            self.get_cell(cell.x + 1, cell.y),
            self.get_cell(cell.x,     cell.y + 1),
            self.get_cell(cell.x - 1, cell.y),
        ]))

    def valid_coordinates(self, x: int, y: int) -> bool:
        return 0 <= x < self.cell_row_size and 0 <= y < self.cell_row_size

    def get_cell(self, x: int, y: int) -> Cell | None:
        if self.valid_coordinates(x, y):
            return self.cells[y][x]

    def recursive_backtracking(self):
        start_cell = self.get_cell(0, 0)
        start_cell.mark_visited()
        stack: list[Cell] = [start_cell]
        while stack:
            current = stack.pop()
            neighbours = self.get_neighbours(current)
            if neighbours:
                stack.append(current)
                next_cell = rnd.choice(neighbours)
                remove_walls(current, next_cell)
                next_cell.mark_visited()
                stack.append(next_cell)

    def __str__(self):
        builder = []
        for y, row in enumerate(self.cells):
            if y == 0:
                builder.append("".join(cell.top_row for cell in row))
            builder.append("".join(cell.mid_row for cell in row))
            builder.append("".join(cell.bot_row for cell in row))
        return "\n".join(builder)
