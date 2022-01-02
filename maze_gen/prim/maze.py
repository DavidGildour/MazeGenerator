import random
from typing import Literal

from maze_gen import Maze
from maze_gen.prim.wall import Wall
from maze_gen.prim.cell import Cell


class PrimMaze(Maze):
    def __init__(self, size: int):
        super(PrimMaze, self).__init__(size, "Prim")
        self.cells = [
            [Cell(x, y) for x in range(self.cell_row_size)]
            for y in range(self.cell_row_size)
        ]
        self.add_walls()

    @staticmethod
    def get_unvisited_cell_from_wall(wall: Wall) -> Cell | None:
        if not wall.cell_a.visited:
            return wall.cell_a
        elif not wall.cell_b.visited:
            return wall.cell_b

    @staticmethod
    def add_wall_to_cells(
        cell_a: Cell, cell_b: Cell, orientation: Literal["hor", "ver"]
    ):
        wall = Wall(cell_a, cell_b)
        dir_a: Literal["e", "s"]
        dir_b: Literal["w", "n"]
        if orientation == "hor":
            dir_a, dir_b = "ew"
        elif orientation == "ver":
            dir_a, dir_b = "sn"
        else:
            raise ValueError("Orientation must one of: 'hor', 'ver'.")
        cell_a.add_wall(wall, dir_a)
        cell_b.add_wall(wall, dir_b)

    def add_walls(self):
        for row in self.cells:
            for cell_a, cell_b in zip(row, row[1:]):
                self.add_wall_to_cells(cell_a, cell_b, "hor")
        for col in zip(*self.cells):
            for cell_a, cell_b in zip(col, col[1:]):
                self.add_wall_to_cells(cell_a, cell_b, "ver")

    def generate(self):
        start_cell = self.cells[0][0]
        start_cell.mark_visited()
        wall_list = [*start_cell.walls]
        while wall_list:
            wall_pick = random.choice(wall_list)
            unvisited_cell = self.get_unvisited_cell_from_wall(wall_pick)
            if unvisited_cell:
                unvisited_cell.mark_visited()
                wall_pick.brake()
                wall_list.extend(
                    wall for wall in unvisited_cell.walls if not wall.broken
                )
            wall_list.remove(wall_pick)

    def __str__(self):
        builder = ["#" * self.total_grid_size]
        for row in self.cells:
            cell_row_str = ["#"]
            wall_row_str = ["#"]
            for cell in row:
                cell_row_str.append(str(cell) + str(cell.east_wall))
                wall_row_str.append(str(cell.south_wall) + "#")

            builder.extend(["".join(cell_row_str), "".join(wall_row_str)])

        return "\n".join(builder)
