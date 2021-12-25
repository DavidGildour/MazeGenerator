from datetime import datetime

from maze_gen import KruskalMaze, RecursiveBacktrackMaze
from prompts import init_questions, print_questions, prompt


algorithms = {
    "Kruskal": KruskalMaze,
    "Recursive Backtracking": RecursiveBacktrackMaze
}


def main():
    answers = prompt(init_questions)
    size = answers.get("size")
    alg_name = answers.get("algorithm")
    algorithm = algorithms[alg_name]
    maze = algorithm(size)
    maze.generate()

    answers = prompt(print_questions)
    if answers["save"]:
        file_name = answers["file_name"] + ".txt"
        header_text = f"-------- MAZE GENERATED ON {datetime.today()} USING '{alg_name}' ALGORITHM --------"
        fill = len(header_text)
        header = "\n".join([
            "-" * fill,
            header_text,
            "-" * fill,
            "\n"
        ])
        with open(file_name, "w") as f:
            f.writelines(header)
            f.writelines(str(maze))
        print(f"Successfully written a {size}x{size} maze to the file '{file_name}'.")


if __name__ == '__main__':
    main()
