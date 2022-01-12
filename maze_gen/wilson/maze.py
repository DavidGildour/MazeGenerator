import random
from dataclasses import dataclass
from enum import Enum
from itertools import chain

from maze_gen import Maze


WALL = "#"
WALL_N = 0b1000
WALL_E = 0b0100
WALL_S = 0b0010
WALL_W = 0b0001


class Direction(Enum):
    N = 0
    E = 1
    S = 2
    W = 3


direction_map = {
    Direction.N: (0, -1),
    Direction.E: (1, 0),
    Direction.S: (0, 1),
    Direction.W: (-1, 0),
}


@dataclass
class Cell:
    x: int
    y: int
    included: bool = False
    walls: int = WALL_N | WALL_S | WALL_W | WALL_E
    direction: Direction | None = None

    @property
    def top_row(self) -> str:
        col_skip = self.x == 0
        return "".join([WALL * col_skip, self.print_wall(WALL_N), WALL])

    @property
    def mid_row(self) -> str:
        col_skip = self.x == 0
        return "".join(
            [self.print_wall(WALL_W) * col_skip, ".", self.print_wall(WALL_E)]
        )

    @property
    def bot_row(self) -> str:
        col_skip = self.x == 0
        return "".join([WALL * col_skip, self.print_wall(WALL_S), WALL])

    def connect(self, neighbouring_cell: "Cell", direction: Direction):
        match direction:
            case Direction.N:
                self.walls -= WALL_N
                neighbouring_cell.walls -= WALL_S
            case Direction.E:
                self.walls -= WALL_E
                neighbouring_cell.walls -= WALL_W
            case Direction.W:
                self.walls -= WALL_W
                neighbouring_cell.walls -= WALL_E
            case Direction.S:
                self.walls -= WALL_S
                neighbouring_cell.walls -= WALL_N

    def print_wall(self, wall: int) -> str:
        return WALL if self.wall_exists(wall) else "."

    def wall_exists(self, wall: int) -> bool:
        return bool(self.walls & wall)


class WilsonMaze(Maze):
    def __init__(self, size: int):
        super(WilsonMaze, self).__init__(size, "Wilson's")
        self.cells = [
            [Cell(x, y) for x in range(self.cell_row_size)]
            for y in range(self.cell_row_size)
        ]

    def get(self, x: int, y: int) -> Cell | None:
        if self.coordinates_are_valid(x, y):
            return self.cells[y][x]

    def coordinates_are_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.cell_row_size and 0 <= y < self.cell_row_size

    def get_neighbours(self, cell: Cell) -> list[tuple[Cell, Direction]]:
        return list(
            filter(
                lambda t: t[0] is not None,
                [
                    (self.get(cell.x + dx, cell.y + dy), direction)
                    for direction, (dx, dy) in direction_map.items()
                ],
            )
        )

    def do_random_walk(self, cell_a: Cell) -> list[Cell]:
        current = cell_a
        visited_cells = [current]
        while not current.included:
            next_cell, direction = random.choice(self.get_neighbours(current))
            current.direction = direction
            current = next_cell
            visited_cells.append(next_cell)

        return visited_cells

    def get_next_cell_from_direction(self, cell: Cell) -> Cell:
        if cell.direction is None:
            raise ValueError(f"Cell <<{cell}>> has no set direction.")
        dx, dy = direction_map[cell.direction]
        return self.get(cell.x + dx, cell.y + dy)

    def connect_cells(self, cell_a: Cell, cell_b: Cell):
        current = cell_a
        while current != cell_b:
            next_cell = self.get_next_cell_from_direction(current)
            current.connect(next_cell, current.direction)
            current.included = True
            current = next_cell

    def generate(self):
        rand_x, rand_y = random.randrange(self.cell_row_size), random.randrange(
            self.cell_row_size
        )
        starting_cell = self.get(rand_x, rand_y)
        starting_cell.included = True

        while cells_left := list(
            filter(lambda c: not c.included, chain.from_iterable(self.cells))
        ):
            current_cell = random.choice(cells_left)
            visited_cells = self.do_random_walk(current_cell)
            ending_cell = visited_cells[-1]
            self.connect_cells(current_cell, ending_cell)

            for cell in visited_cells:
                cell.direction = None

    def __str__(self):
        builder = []
        for y, row in enumerate(self.cells):
            if y == 0:
                builder.append("".join(cell.top_row for cell in row))
            builder.append("".join(cell.mid_row for cell in row))
            builder.append("".join(cell.bot_row for cell in row))
        return "\n".join(builder)
