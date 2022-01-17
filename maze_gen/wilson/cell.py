from dataclasses import dataclass

from maze_gen.wilson.direction import Direction

WALL = "#"
WALL_N = 0b1000
WALL_E = 0b0100
WALL_S = 0b0010
WALL_W = 0b0001


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
