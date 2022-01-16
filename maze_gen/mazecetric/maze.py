from maze_gen import Maze
from maze_gen.mazecetric.cell import Cell, RuleSet, Board


class MazecetricMaze(Maze):
    """
    Creates a maze based on a Game Of Life algorithm with a modified rule set.
    """

    ALIVE_CHANCE = 0.5

    def __init__(self, size: int):
        super(MazecetricMaze, self).__init__(size, "Mazecetric")
        self.rule_set = RuleSet("Mazecetric", a_rules=(1, 2, 3, 4), d_rules=(3,))
        self.board = Board(self.ALIVE_CHANCE, self.total_grid_size)

    def will_be_alive(self, cell) -> bool:
        neighbours = self.get_neighbours(cell)
        c = len(neighbours)
        if not cell.is_alive and c in self.rule_set.dead_rules:
            return True
        elif cell.is_alive and c in self.rule_set.alive_rules:
            return True
        return False

    def generate(self):
        for _ in range(self.total_grid_size * 2):
            next_gen = Board(0, self.total_grid_size)
            for i, row in enumerate(self.board):
                for cell in row:
                    # dont touch the side walls
                    if (
                        0 < cell.x < self.total_grid_size - 1
                        and 0 < cell.y < self.total_grid_size - 1
                    ):
                        next_gen.set_cell(cell.x, cell.y, self.will_be_alive(cell))
            self.board = next_gen

    def get_neighbours(self, cell) -> list[Cell]:
        """
                 y
        x   -1, -1 |  0, -1  | +1, -1
            -1,  0 |  [cell] | +1,  0
            -1, +1 |  0, +1, | +1, +1
        """
        cells = []
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                if x_offset == 0 and y_offset == 0:
                    continue  # we dont want to check the cell itself as a neighbour
                cells.append(self.board.get_cell(cell.x + x_offset, cell.y + y_offset))

        return list(filter(None, cells))

    def __str__(self):
        maze_str = ""
        for row in self.board:
            maze_str += "".join([str(c) for c in row])
            maze_str += "\n"
        return maze_str.rstrip("\n")
