class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.cell_set: set[Cell] = {self}

    @property
    def coor(self) -> tuple[int, int]:
        return self.x, self.y

    def __hash__(self) -> int:
        return hash(self.coor)

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

    def __str__(self):
        return "."
