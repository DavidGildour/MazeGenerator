from maze_gen import KruskalMaze, RecursiveBacktrackMaze
from prompts import init_questions, print_questions, prompt


algorithms = {
    "Kruskal": KruskalMaze,
    "Recursive Backtracking": RecursiveBacktrackMaze
}


def main():
    answers = prompt(init_questions)
    size = answers.get("size")
    algorithm = algorithms[answers.get("algorithm")]
    maze = algorithm(size)
    maze.generate()

    answers = prompt(print_questions)
    if answers["save"]:
        file_name = answers["file_name"] + ".txt"
        with open(file_name, "w") as f:
            f.writelines(str(maze))
        print(f"Successfully written a {size}x{size} maze to the file '{file_name}'.")


if __name__ == '__main__':
    main()
