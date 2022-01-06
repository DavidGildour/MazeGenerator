from abc import ABC

MIN_MAZE_SIZE = 5


class Maze(ABC):
    def __init__(self, size: int, name: str):
        if not size % 2 or size < MIN_MAZE_SIZE:
            raise ValueError(
                f"In order for the maze pattern to be symmetrical and readable, "
                f"the size must be odd and at least {MIN_MAZE_SIZE}. Given size: {size}"
            )
        self.alg_name = name
        self.total_grid_size = size
        self.cell_row_size = size // 2

    def generate(self):
        raise NotImplementedError
