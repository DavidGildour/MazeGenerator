from dataclasses import dataclass

WALL = "#"
N = 0b1000
E = 0b0100
S = 0b0010
W = 0b0001


def remove_walls(c1: "Cell", c2: "Cell"):
    if c1.x > c2.x:    # left > WE
        c1.crash_wall(W)
        c2.crash_wall(E)
    elif c1.x < c2.x:  # right > EW
        c1.crash_wall(E)
        c2.crash_wall(W)
    elif c1.y > c2.y:  # up > NS
        c1.crash_wall(N)
        c2.crash_wall(S)
    elif c1.y < c2.y:  # down > SN
        c1.crash_wall(S)
        c2.crash_wall(N)


@dataclass
class Cell:
    x: int
    y: int
    visited: bool = False
    walls: int = N | E | S | W

    @property
    def coor(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def top_row(self) -> str:
        col_skip = self.x == 0
        return "".join([WALL * col_skip, self.print_wall(N), WALL])

    @property
    def mid_row(self) -> str:
        col_skip = self.x == 0
        return "".join([self.print_wall(W) * col_skip, " ", self.print_wall(E)])

    @property
    def bot_row(self) -> str:
        col_skip = self.x == 0
        return "".join([WALL * col_skip, self.print_wall(S), WALL])

    def mark_visited(self):
        self.visited = True

    def print_wall(self, wall: int) -> str:
        return WALL if self.wall_exists(wall) else " "

    def crash_wall(self, wall: int):
        self.walls -= wall

    def wall_exists(self, wall: int) -> bool:
        return bool(self.walls & wall)

    def __hash__(self):
        return hash(self.coor)
