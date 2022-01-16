import random

from maze_gen import Maze
from maze_gen.recursive_division.wall import Wall


Chamber = tuple[tuple[int, int], tuple[int, int]]
Orientation = int

HORIZONTAL = 0
VERTICAL = 1


class RecursiveDivisionMaze(Maze):
    def __init__(self, size: int):
        super(RecursiveDivisionMaze, self).__init__(size, "Recursive Division")
        self.wall_row_size = self.cell_row_size + 1
        self.wall_dict: dict[tuple[int, int], Wall] = dict()
        self.wall_rows = self.init_wall_rows()
        self.wall_cols = self.init_wall_cols()

    def get_wall(self, x: int, y: int) -> Wall:
        wall = self.wall_dict.get((x, y))
        if wall is None:
            wall = Wall(x, y, self.wall_is_border(x, y))
            self.wall_dict[(x, y)] = wall
        return wall

    def init_wall_rows(self):
        return [
            [self.get_wall(x, y) for x in range(self.total_grid_size)]
            for y in range(0, self.total_grid_size, 2)
        ]

    def init_wall_cols(self):
        return [
            [self.get_wall(x, y) for y in range(self.total_grid_size)]
            for x in range(0, self.total_grid_size, 2)
        ]

    def wall_is_border(self, x: int, y: int) -> bool:
        return x in (0, self.total_grid_size - 1) or y in (0, self.total_grid_size - 1)

    def get_wall_row(self, y: int, x_range: tuple[int, int]) -> list[Wall]:
        x1, x2 = x_range
        return self.wall_rows[y][x1 * 2 : x2 * 2]

    def get_wall_column(self, x: int, y_range: tuple[int, int]) -> list[Wall]:
        y1, y2 = y_range
        return self.wall_cols[x][y1 * 2 : y2 * 2]

    @staticmethod
    def place_walls_with_random_passage(wall_line: list[Wall]):
        passage_index = random.randrange(1, len(wall_line), 2)
        for i, wall in enumerate(wall_line):
            if i != passage_index:
                wall.erect()

    @staticmethod
    def determine_orientation(width: int, height: int) -> Orientation:
        if width > height:
            return VERTICAL
        elif height > width:
            return HORIZONTAL
        else:
            return random.choice((VERTICAL, HORIZONTAL))

    def divide_chamber(self, chamber: Chamber):
        x_range, y_range = chamber
        x_min, x_max = x_range
        y_min, y_max = y_range
        width, height = x_max - x_min, y_max - y_min
        orientation = self.determine_orientation(width, height)
        if orientation == VERTICAL:
            if x_max - x_min < 2:
                return
            x = random.randrange(x_min + 1, x_max)

            column = self.get_wall_column(x, (y_min, y_max))
            self.place_walls_with_random_passage(column)

            left_subchamber = ((x_min, x), chamber[1])
            self.divide_chamber(left_subchamber)
            right_subchamber = ((x, x_max), chamber[1])
            self.divide_chamber(right_subchamber)
        elif orientation == HORIZONTAL:
            if y_max - y_min < 2:
                return
            y = random.randrange(y_min + 1, y_max)

            row = self.get_wall_row(y, (x_min, x_max))
            self.place_walls_with_random_passage(row)

            top_subchamber = (chamber[0], (y_min, y))
            self.divide_chamber(top_subchamber)
            bottom_subchamber = (chamber[0], (y, y_max))
            self.divide_chamber(bottom_subchamber)

    def generate(self):
        start_chamber = ((0, self.wall_row_size - 1), (0, self.wall_row_size - 1))
        self.divide_chamber(start_chamber)

    def __str__(self):
        builder = []
        for i, row in enumerate(self.wall_rows):
            builder.append("".join(str(wall) for wall in row))
            if i < self.wall_row_size - 1:
                builder.append(
                    ".".join(str(wall_col[2 * i + 1]) for wall_col in self.wall_cols)
                )
        return "\n".join(builder)
