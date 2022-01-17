from maze_gen.mazecetric.cell import Cell, Board


def test_init():
    c = Cell(1, 2, True)
    assert c.x == 1
    assert c.y == 2
    assert c.coor == (1, 2)
    assert c.is_alive
    assert bool(c)


def test_board_init():
    b = Board(1, 10)
    assert b.board_side == 10
    assert all(b.cells)


def test_board_get_cell():
    b = Board(1, 10)
    assert b.get_cell(5, 5).is_alive
    assert b.get_cell(13, 13) is None
    assert b.get_cell(10, 10) is None
    assert b.get_cell(0, 0).is_alive
    assert b.get_cell(-1, 5) is None
    assert b.get_cell(4, 14) is None
