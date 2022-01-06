from random import random


class Cell:
    x: int
    y: int
    coor: tuple
    is_alive: bool
    init_seed: float

    def __init__(self, x: int, y: int, alive: bool):
        self.x = x
        self.y = y
        self.is_alive = alive
        self.coor = (x, y)

    def __str__(self):
        return "#" if self.is_alive else "."


class RuleSet:
    alive_rules: tuple
    dead_rules: tuple
    name: str

    def __init__(self, name: str, a_rules: tuple, d_rules: tuple):
        self.alive_rules = a_rules
        self.dead_rules = d_rules
        self.name = name


class Board:
    cells: list[list[Cell]]
    board_side: int

    def __init__(self, alive_chance: float, total_grid_size: int):
        self.board_side = total_grid_size
        self.cells: list[list[Cell]] = []
        for y in range(self.board_side):
            self.cells.append([])
            for x in range(self.board_side):
                if 0 < x < self.board_side - 1 and 0 < y < self.board_side - 1:
                    self.cells[y].append(Cell(x, y, random() <= alive_chance))
                else:
                    # side walls are always alive
                    self.cells[y].append(Cell(x, y, True))

    def __iter__(self):
        return iter(self.cells)

    def get_cell(self, x: int, y: int) -> Cell:
        if x < 0 or y < 0:
            raise IndexError("Cannot lookup negative indices.")
        return self.cells[y][x]

    def set_cell(self, x: int, y: int, alive: bool):
        self.cells[y][x] = Cell(x, y, alive)
