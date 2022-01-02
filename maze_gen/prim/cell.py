from dataclasses import dataclass, field
from typing import Literal

from maze_gen.kruskal.wall import Wall


@dataclass
class WallDict:
    north: Wall = None
    east: Wall = None
    south: Wall = None
    west: Wall = None

    @property
    def wall_list(self) -> list[Wall]:
        return [self.north, self.east, self.south, self.west]

    def as_list(self) -> list[Wall]:
        return list(filter(None, self.wall_list))

    def __repr__(self):
        return "".join(str(wall or "#") for wall in self.wall_list)


@dataclass
class Cell:
    x: int
    y: int
    visited: bool = False
    _walls: WallDict = field(default_factory=WallDict)

    @property
    def north_wall(self) -> Wall | str:
        return self._walls.north or "#"

    @property
    def east_wall(self) -> Wall:
        return self._walls.east or "#"

    @property
    def south_wall(self) -> Wall:
        return self._walls.south or "#"

    @property
    def west_wall(self) -> Wall:
        return self._walls.west or "#"

    @property
    def walls(self) -> list[Wall]:
        return self._walls.as_list()

    def add_wall(self, wall: Wall, direction: Literal["n", "e", "w", "s"]):
        match direction:
            case "n":
                self._walls.north = wall
            case "e":
                self._walls.east = wall
            case "w":
                self._walls.west = wall
            case "s":
                self._walls.south = wall
            case _:
                raise ValueError("The direction must be one of: 'n', 'e', 'w', 's'.")

    def mark_visited(self):
        self.visited = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y}, walls={self._walls}"

    def __str__(self):
        return "."
