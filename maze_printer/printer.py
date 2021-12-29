from datetime import datetime
from math import log, floor
from os import PathLike

from maze_gen import Maze


def generate_header(
    alg_name: str,
    max_width: int = 70,
    dt: datetime = datetime.today(),
    fill_ch: str = "-",
) -> list[str]:
    header_text = [f"MAZE GENERATED ON {str(dt)[:19]}", f"USING '{alg_name}' ALGORITHM"]
    if len(" ".join(header_text)) <= max_width - 8:
        header_text = [" ".join(header_text)]

    fmt_str = f"{{:{fill_ch}<{max_width-4}}}"
    header = [fill_ch * 3 + f" {fmt_str.format(msg + ' ')}" for msg in header_text]

    return [fill_ch * max_width, *header, fill_ch * max_width]


def prepare_maze(maze: Maze) -> list[str]:
    maze_str = str(maze)
    maze_rows = maze_str.split("\n")
    maze_size = maze.total_grid_size
    max_digits = floor(log(maze_size, 10)) + 1
    total_line_length = (max_digits + 5) * 2 + maze_size

    def format_row_num(_i: int, left: bool = True) -> str:
        checkbox = "[ ]"
        pad = ">" if left else "<"
        _fmt_str = f"{{:{pad}{max_digits}}}"

        builder = [
            (
                " " * max_digits
                if _i != maze_size - 1 and _i % 5
                else _fmt_str.format(f"{_i}")
            )
        ]
        if left:
            builder.insert(0, checkbox)
        else:
            builder.append(checkbox)

        return " ".join(builder)

    def generate_col_enum(top: bool = True):
        pad = ">" if top else "<"
        col_fmt_str = f"{{:^{total_line_length}}}"
        col_enum_rows = [[] for _ in range(max_digits)]
        for i in range(maze_size):
            if i != maze_size - 1 and i % 5:
                for col in col_enum_rows:
                    col.append(" ")
            else:
                i_fmt_str = f"{{:{pad}{max_digits}}}"
                str_i = i_fmt_str.format(i)

                for j, ch in enumerate(str_i):
                    col_enum_rows[j].append(ch)

        return [col_fmt_str.format("".join(col_enum)) for col_enum in col_enum_rows]

    top_col_enum = generate_col_enum()
    bot_col_enum = generate_col_enum(top=False)

    formatted_rows = [
        " ".join([format_row_num(i), row, format_row_num(i, left=False)])
        for i, row in enumerate(maze_rows)
    ]
    return top_col_enum + formatted_rows + bot_col_enum


def generate_text_file_for(maze: Maze, **header_kwargs) -> str:
    header = generate_header(maze.alg_name, **header_kwargs)
    prepared_maze = prepare_maze(maze)

    return "\n".join(header + ["\n"] + prepared_maze)


def save_maze_to_file(maze: Maze, file_name: PathLike, **header_kwargs):
    file_content = generate_text_file_for(maze, **header_kwargs)
    with open(file_name, "w") as f:
        f.writelines(file_content)
