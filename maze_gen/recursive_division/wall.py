from dataclasses import dataclass


@dataclass
class Wall:
    x: int
    y: int
    exists: bool = False

    def erect(self):
        self.exists = True

    def __str__(self):
        return "#" if self.exists else "."
