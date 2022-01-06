from maze_gen import Maze
from maze_gen.mazecetric.cell import Cell, RuleSet, Board


class MazecetricMaze(Maze):
    """
    FOR SHAIIBON:
    The main thing you need to implement is the `generate()` and `__str__()` methods. The first - obviously, should
    generate the previously initialized maze (and change the object's inner state, not return anything). The second will
    be used for maze printing, so it needs to follow the strict interface - the returned string, representing the
    maze, needs to include the outside walls and inner passages. The walls should be always represented by '#'
    character, and the passages by the '.' character. Remember that the total size of the maze (i.e. the number of
    characters representing the single row in the output string) will always be odd. Good luck!
    """

    ALIVE_CHANCE = 0.5

    def __init__(self, size: int):
        super(MazecetricMaze, self).__init__(size, "Mazecetric")
        self.rule_set = RuleSet("Mazecetric", a_rules=(1, 2, 3, 4), d_rules=(3,))
        self.board = Board(self.ALIVE_CHANCE, self.total_grid_size)

    def will_survive(self, cell) -> bool:
        c = self.count_alive_neighbours(cell)
        if not cell.is_alive and c in self.rule_set.dead_rules:
            return True
        elif cell.is_alive and c in self.rule_set.alive_rules:
            return True
        return False

    def generate(self):
        for _ in range(100):
            next_gen = Board(0, self.total_grid_size)
            for i, row in enumerate(self.board):
                for cell in row:
                    # dont touch the side walls
                    if (
                        0 < cell.x < self.total_grid_size - 1
                        and 0 < cell.y < self.total_grid_size - 1
                    ):
                        next_gen.set_cell(cell.x, cell.y, self.will_survive(cell))
            self.board = next_gen

    def count_alive_neighbours(self, cell):
        """
                 y
        x   -1, -1 |  0, -1  | +1, -1
            -1,  0 |  [cell] | +1,  0
            -1, +1 |  0, +1, | +1, +1
        """
        count = 0
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                if x_offset == 0 and y_offset == 0:
                    continue  # we dont want to check the cell itself as a neighbour
                try:
                    if self.board.get_cell(
                        cell.x + x_offset, cell.y + y_offset
                    ).is_alive:
                        count += 1
                except IndexError:
                    continue

        return count

    def __str__(self):
        maze_str = ""
        for row in self.board:
            maze_str += "".join([str(c) for c in row])
            maze_str += "\n"
        return maze_str.rstrip("\n")
