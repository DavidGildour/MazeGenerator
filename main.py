import sys

from maze import Maze


def main():
    maze_size = input("Specify the size of the maze: ")
    if not maze_size.isnumeric():
        print("Wrong input")
        sys.exit()
    maze_size = int(maze_size)
    maze = Maze(maze_size)
    maze.recursive_backtracking()
    maze_str = str(maze)

    with open("maze.txt", "w") as f:
        f.writelines(maze_str)


if __name__ == '__main__':
    main()
