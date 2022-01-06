from .cell import Cell


def test_init():
    c = Cell(1, 2, True)
    assert c.x == 1
    assert c.y == 2
    assert c.coor == (1, 2)
    assert c.is_alive
