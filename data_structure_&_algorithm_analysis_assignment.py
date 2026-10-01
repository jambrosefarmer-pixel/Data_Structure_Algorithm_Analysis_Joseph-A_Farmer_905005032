class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if self.items else None

    def peek(self):
        return self.items[-1] if self.items else None

    def is_empty(self):
        return len(self.items) == 0


def precedence(operator):
    if operator in ("+", "-"):
        return 1
    if operator in ("*", "/"):
        return 2
    return 0


def apply_operator(x, y, operator):
    if operator == "+":
        return x + y
    if operator == "-":
        return x - y
    if operator == "*":
        return x * y
    if operator == "/":
        if y == 0:
            raise ZeroDivisionError("division by zero")
        return x / y
    raise ValueError(f"Unknown operator: {operator}")


def process_top(numbers, operators):
    operator = operators.pop()
    y = numbers.pop()
    x = numbers.pop()
    if x is None or y is None:
        raise ValueError("Malformed expression")
    numbers.push(apply_operator(x, y, operator))


def evaluate_mathematical_expression(expression):
    numbers = Stack()
    operators = Stack()
    i = 0
    expect_operand = True

    while i < len(expression):
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        if char.isdigit() or char == "." or (char == "-" and expect_operand):
            start = i
            if char == "-":
                i += 1
            while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                i += 1
            numbers.push(float(expression[start:i]))
            expect_operand = False
            continue

        if char == "(":
            operators.push(char)
            expect_operand = True
        elif char == ")":
            while not operators.is_empty() and operators.peek() != "(":
                process_top(numbers, operators)
            if operators.is_empty():
                raise ValueError("Mismatched parentheses")
            operators.pop()
            expect_operand = False
        elif char in "+-*/":
            while (not operators.is_empty()
                   and operators.peek() != "("
                   and precedence(operators.peek()) >= precedence(char)):
                process_top(numbers, operators)
            operators.push(char)
            expect_operand = True
        else:
            raise ValueError(f"Invalid character: {char}")

        i += 1

    while not operators.is_empty():
        if operators.peek() == "(":
            raise ValueError("Mismatched parentheses")
        process_top(numbers, operators)

    result = numbers.pop()
    if result is None or not numbers.is_empty():
        raise ValueError("Malformed expression")
    return result


def format_result(result):
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)


def is_expression(line):
    """A line is an expression only if it contains at least one digit."""
    return any(c.isdigit() for c in line)


def read_and_evaluate_file():
    results = []
    with open("input.txt", "r", encoding="utf-8-sig") as file:
        for line in file:
            line = line.strip()
            if not is_expression(line):   # blank lines and separators
                continue
            try:
                results.append(format_result(evaluate_mathematical_expression(line)))
            except (ValueError, ZeroDivisionError) as e:
                results.append(f"Error: {e}")
    return results


def write_results_to_file(results):
    result_index = 0
    with open("input.txt", "r", encoding="utf-8-sig") as input_file, \
         open("output.txt", "w") as output_file:
        for line in input_file:
            line = line.strip()
            if not is_expression(line):   # copy blanks and separators unchanged
                output_file.write(line + "\n")
            elif result_index < len(results):
                output_file.write(results[result_index] + "\n")
                result_index += 1


def main():
    results = read_and_evaluate_file()
    print("Results:", results)
    write_results_to_file(results)
    print("Evaluation completed successfully")


if __name__ == "__main__":
    main()