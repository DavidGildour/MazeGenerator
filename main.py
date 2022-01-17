from maze_gen import (
    KruskalMaze,
    RecursiveBacktrackMaze,
    PrimMaze,
    WilsonMaze,
    RecursiveDivisionMaze,
    MazecetricMaze
)
from maze_printer import save_maze_to_file
from prompts import init_questions, print_questions, prompt


algorithms = {
    "Kruskal": KruskalMaze,
    "Recursive Backtracking": RecursiveBacktrackMaze,
    "Prim": PrimMaze,
    "Mazecetric": MazecetricMaze,
    "Wilson": WilsonMaze,
    "Recursive Division": RecursiveDivisionMaze,
}


def main():
    answers = prompt(init_questions)
    size = answers.get("size")
    alg_name = answers.get("algorithm")
    algorithm = algorithms[alg_name]
    maze = algorithm(size)
    maze.generate()
    print(maze)

    answers = prompt(print_questions)
    if answers["save"]:
        file_name = answers["file_name"] + ".txt"
        save_maze_to_file(maze, file_name)
        print(f"Successfully written a {size}x{size} maze to the file '{file_name}'.")


if __name__ == "__main__":
    main()
