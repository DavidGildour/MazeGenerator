from maze_gen import Maze


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

    def __init__(self, size: int):
        super(MazecetricMaze, self).__init__(size, "Mazecetric")
        ...

    def generate(self):
        raise NotImplementedError
