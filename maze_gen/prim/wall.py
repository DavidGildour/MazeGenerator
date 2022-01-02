from dataclasses import dataclass

from maze_gen.prim.cell import Cell


@dataclass
class Wall:
    cell_a: Cell
    cell_b: Cell
    broken: bool = False

    def brake(self):
        self.broken = True

    def __str__(self):
        return "." if self.broken else "#"
