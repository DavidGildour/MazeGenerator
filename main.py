from maze_gen.kruskal.maze import KruskalMaze
from maze_gen.recursive_backtrack import RecursiveBacktrackMaze
from prompts import questions, prompt


algorithms = {
    "Kruskal": KruskalMaze,
    "Recursive Backtracking": RecursiveBacktrackMaze
}


def main():
    answers = prompt(questions)
    size = answers.get("size")
    algorithm = algorithms[answers.get("algorithm")]
    maze = algorithm(size)
    maze.generate()

    print(maze)


if __name__ == '__main__':
    main()
