from abc import ABC


class Maze(ABC):
    def __init__(self, size: int):
        if not size % 2 or size < 5:
            raise ValueError(f"In order for the maze pattern to be symmetrical and readable, "
                             f"the size must be odd and at least 5. Given size: {size}")
        self.total_grid_size = size
        self.cell_row_size = size // 2
