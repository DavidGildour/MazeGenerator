import random
from collections import defaultdict
from dataclasses import dataclass

from maze_gen import Maze


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.cell_set: set[Cell] = {self}

    @property
    def coor(self) -> tuple[int, int]:
        return self.x, self.y

    def __hash__(self) -> int:
        return hash(self.coor)

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

    def __str__(self):
        return " "


@dataclass
class Wall:
    cell_a: Cell
    cell_b: Cell
    row_n: int
    broken: bool = False

    @property
    def linking_cells(self) -> tuple[Cell, Cell]:
        return self.cell_a, self.cell_b

    def brake(self):
        self.broken = True

    def __str__(self):
        return " " if self.broken else "#"


class KruskalMaze(Maze):
    """A maze generator implementing a randomized Kruskal's algorithm"""
    def __init__(self, size: int):
        super(KruskalMaze, self).__init__(size)
        self.cells = [
            [Cell(x, y) for x in range(self.cell_row_size)] for y in range(self.cell_row_size)
        ]
        self.walls = self.generate_walls()

    @property
    def walls_by_row(self) -> dict[int, list[Wall]]:
        d = defaultdict(list)
        for wall in sorted(self.walls, key=lambda w: w.row_n):
            d[wall.row_n].append(wall)
        return d

    def generate_walls(self) -> list[Wall]:
        walls = []
        for row in self.cells:
            for cell_a, cell_b in zip(row, row[1:]):
                walls.append(Wall(cell_a, cell_b, cell_a.y * 2))
        for col in zip(*self.cells):
            for cell_a, cell_b in zip(col, col[1:]):
                walls.append(Wall(cell_a, cell_b, cell_a.y * 2 + 1))
        return walls

    def generate(self):
        shuffled_walls = sorted(self.walls, key=lambda w: random.random())
        for wall in shuffled_walls:
            cell_a, cell_b = wall.linking_cells
            if not cell_a.cell_set & cell_b.cell_set:
                wall.brake()
                joined = cell_a.cell_set | cell_b.cell_set
                cell_a.cell_set = joined
                cell_b.cell_set = joined

    def __str__(self):
        builder = ["#" * self.total_grid_size]
        for row_n, walls in self.walls_by_row.items():
            row_str = "#"
            if row_n % 2:
                row_str += "#".join(str(wall) for wall in walls)
            else:
                for wall in walls:
                    cell_a, cell_b = wall.linking_cells
                    if cell_a.x == 0:
                        row_str += str(cell_a)
                    row_str += str(wall) + str(cell_b)
            row_str += "#"
            builder.append(row_str)
        builder.append("#" * self.total_grid_size)

        return "\n".join(builder)
