init_questions = [
    {
        "type": "input_int",
        "name": "size",
        "message": "Specify the size of the maze:",
        "validate": lambda x: 5 <= x and x % 2,
        "validate_message": "A size must be an odd integer greater than 4.",
        "default": 51,
    },
    {
        "type": "list",
        "name": "algorithm",
        "message": "Which algorithm do you want to use?",
        "choices": [
            "Kruskal",
            "Recursive Backtracking",
            "Prim",
            "Mazecetric",
            "Wilson",
            "Recursive Division",
        ],
    },
]


print_questions = [
    {
        "type": "bool",
        "name": "save",
        "message": "Do you want to save the maze to the file?",
        "default": True,
    },
    {
        "type": "input",
        "name": "file_name",
        "message": "Specify the name of the file:",
        "depends_on": "save",
    },
]


def prompt_question(question: dict, answers: dict):
    if dependency := question.get("depends_on"):
        if not answers.get(dependency):
            return
    msg = question.get("message")
    if not msg:
        raise ValueError("A question must have a message")
    if not msg.endswith(" "):
        msg += " "

    question_type = question.get("type")
    if not msg:
        raise ValueError("A question must have a type")

    name = question.get("name")
    if not name:
        raise ValueError("A question must have a name")

    valid = question.get("validate")
    valid_message = question.get("validate_message")
    default = question.get("default")

    result = None
    if question_type == "input":
        if default is not None:
            msg += f"(default: {default}) "
        while not result:
            raw_input = input(msg)
            if not raw_input and default is not None:
                answers[name] = default
                return
            if raw_input:
                if valid is not None and not valid(raw_input):
                    error_message = "Invalid input. "
                    if valid_message:
                        error_message += valid_message
                    print(error_message)
                else:
                    result = raw_input
            else:
                print("You need to specify some value.")
    elif question_type == "bool":
        if default is not None:
            default_repr = " (Y/n) " if default is True else "(y/N) "
            msg += default_repr
        while result is None:
            raw_input = input(msg)
            if raw_input.lower() in {"n", "no"}:
                result = False
            elif not raw_input:
                if default is not None:
                    result = default
                else:
                    print("You need to make a choice.")
            else:
                result = True
    elif question_type == "input_int":
        if default is not None:
            msg += f"(default: {default}) "
        while not result:
            raw_input = input(msg)
            if not raw_input and default is not None:
                answers[name] = default
                return
            if raw_input.isdigit():
                parsed_input = int(raw_input)
                if valid is not None and not valid(parsed_input):
                    error_message = "Invalid input. "
                    if valid_message:
                        error_message += valid_message
                    print(error_message)
                else:
                    result = parsed_input
            else:
                print("The value must be an integer.")
    elif question_type == "list":
        choices = question.get("choices")
        print(msg)
        for i, choice in enumerate(choices, 1):
            print(f"\t{i}. " + choice)
        while not result:
            raw_input = input("Choose one of the options above: ")
            if raw_input.isdigit():
                parsed_input = int(raw_input)
                if parsed_input in range(1, len(choices) + 1):
                    result = choices[parsed_input - 1]
                else:
                    print(
                        f"Your choice must be an integer in range {1}-{len(choices)}."
                    )
            else:
                print("The value must be an integer.")

    answers[name] = result


def prompt(prompt_questions: list[dict]) -> dict:
    answers = dict()
    for q in prompt_questions:
        prompt_question(q, answers)
    return answers
