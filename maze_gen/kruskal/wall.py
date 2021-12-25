from dataclasses import dataclass

from maze_gen.kruskal.cell import Cell


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
        return "." if self.broken else "#"

