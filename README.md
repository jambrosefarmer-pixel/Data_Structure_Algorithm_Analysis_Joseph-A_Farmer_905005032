# Stack-Based Mathematical Expression Evaluator

A Python program that reads mathematical expressions from a text file, evaluates each one using a **stack-based algorithm** (a variant of Dijkstra's shunting-yard method), and writes the results to an output file while preserving the layout of the original file (blank lines and separator lines stay exactly where they were).

---

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Project Structure](#project-structure)
4. [Getting Started](#getting-started)
5. [Input File Format](#input-file-format)
6. [Output File Format](#output-file-format)
7. [Full Example](#full-example)
8. [How It Works](#how-it-works)
9. [Code Reference](#code-reference)
10. [Error Handling](#error-handling)
11. [Limitations](#limitations)
12. [Troubleshooting](#troubleshooting)
13. [Possible Improvements](#possible-improvements)
14. [License](#license)

---

## Features

- Evaluates expressions using a custom `Stack` class (no `eval()`, so it is safe on untrusted input).
- Supports the four basic operators: `+`, `-`, `*`, `/`.
- Correct **operator precedence**: `*` and `/` are applied before `+` and `-`.
- Supports **parentheses**, including nested ones, e.g. `((2 + 3) * (4 - 1))`.
- Supports **decimal numbers**, e.g. `2.5 * 4`.
- Supports **negative numbers** (unary minus), e.g. `-3 + 5` or `2 * (-4)`.
- Ignores spaces anywhere in an expression.
- Preserves blank lines and separator lines (such as `_ _ _ _ _ _`) in the output.
- Reports problems per line (division by zero, mismatched parentheses, invalid characters) without crashing the whole run.
- Prints whole-number results as integers (`13`, not `13.0`).

---

## Requirements

- Python **3.6 or newer** (uses f-strings).
- No third-party libraries. Only the Python standard library is used.

Check your version with:

```bash
python --version
```

---

## Project Structure

```
project-folder/
├── main.py        # The program (name it whatever you like)
├── input.txt      # Your expressions (you create this)
├── output.txt     # Generated results (created automatically)
└── README.md      # This file
```

> **Important:** `input.txt` and `output.txt` are read from and written to the folder you run the command from (the *current working directory*), not necessarily the folder where the script is stored. Run the script from inside the project folder.

---

## Getting Started

1. **Save the program** as `main.py` (or any name you prefer).
2. **Create `input.txt`** in the same folder and add your expressions (see the format below).
3. **Run the program:**

   ```bash
   python main.py
   ```

4. **Read the results** in the console and in the generated `output.txt`.

Expected console output for the example below:

```
Results: ['13', '16', '-10']
Evaluation completed successfully
```

---

## Input File Format

`input.txt` is a plain text file with one expression per line. Three kinds of lines are recognised:

| Line type | Description | What happens |
|---|---|---|
| **Expression** | Any line containing at least one digit, e.g. `3 + 5 * 2` | Evaluated; the result replaces the line in the output |
| **Separator** | A line with no digits, e.g. `_ _ _ _ _ _` or `__________` | Copied to the output unchanged |
| **Blank line** | An empty line | Copied to the output unchanged |

### Valid characters inside an expression

- Digits `0-9`
- Decimal point `.`
- Operators `+ - * /`
- Parentheses `( )`
- Spaces (ignored)

Any other character (for example a letter) produces an error message for that line.

---

## Output File Format

`output.txt` mirrors `input.txt` line by line:

- Each expression line is replaced by its result.
- Blank lines stay blank.
- Separator lines are copied exactly.
- If an expression is invalid, its line contains `Error: <reason>` instead of a result.

---

## Full Example

**input.txt**

```
3 + 5 * 2
_ _ _ _ _ _

(8 / 4) + 7 * 2

_ _ _ _ _ _

10 - (2 + 3) * 4
```

**output.txt**

```
13
_ _ _ _ _ _

16

_ _ _ _ _ _

-10
```

### Step-by-step check

| Expression | Working | Result |
|---|---|---|
| `3 + 5 * 2` | `5 * 2 = 10`, then `3 + 10` | `13` |
| `(8 / 4) + 7 * 2` | `8 / 4 = 2`, `7 * 2 = 14`, `2 + 14` | `16` |
| `10 - (2 + 3) * 4` | `2 + 3 = 5`, `5 * 4 = 20`, `10 - 20` | `-10` |

---

## How It Works

The evaluator uses **two stacks**:

- a **number stack** that holds operands, and
- an **operator stack** that holds operators and opening parentheses.

The expression is scanned from left to right, one character at a time:

1. **Spaces** are skipped.
2. **Numbers** (including decimals and a leading minus sign when a number is expected) are read in full and pushed onto the number stack.
3. **`(`** is pushed onto the operator stack.
4. **`)`** causes operators to be applied until the matching `(` is found; the `(` is then discarded.
5. **An operator** (`+ - * /`) first applies any operators already on the stack that have **higher or equal precedence**, and is then pushed itself.
6. After the whole expression has been scanned, any remaining operators are applied.
7. The single value left on the number stack is the result.

### Applying one operator

To apply an operator, the program pops the operator, then pops two numbers. The **first number popped is the right-hand operand** and the second is the left-hand operand, which matters for `-` and `/`:

```
numbers: [10, 4]   operator: "-"
y = 4   (popped first)
x = 10  (popped second)
result = x - y = 6
```

### Operator precedence

| Operator | Precedence |
|---|---|
| `+`, `-` | 1 |
| `*`, `/` | 2 |
| `(` | 0 (never applied directly) |

Operators of equal precedence are evaluated **left to right**, so `10 - 4 - 3` gives `3`, not `9`.

### Worked trace: `3 + 5 * 2`

| Step | Character | Number stack | Operator stack | Action |
|---|---|---|---|---|
| 1 | `3` | `[3]` | `[]` | push number |
| 2 | `+` | `[3]` | `[+]` | push operator |
| 3 | `5` | `[3, 5]` | `[+]` | push number |
| 4 | `*` | `[3, 5]` | `[+, *]` | `*` outranks `+`, so just push |
| 5 | `2` | `[3, 5, 2]` | `[+, *]` | push number |
| End | | `[3, 10]` | `[+]` | apply `*` |
| End | | `[13]` | `[]` | apply `+` |

---

## Code Reference

### `class Stack`

A minimal stack backed by a Python list.

| Method | Description |
|---|---|
| `push(item)` | Adds an item to the top |
| `pop()` | Removes and returns the top item, or `None` if empty |
| `peek()` | Returns the top item without removing it, or `None` if empty |
| `is_empty()` | Returns `True` if the stack has no items |

### Functions

| Function | Purpose |
|---|---|
| `precedence(operator)` | Returns the precedence level of an operator |
| `apply_operator(x, y, operator)` | Performs `x <operator> y`; raises `ZeroDivisionError` for division by zero |
| `process_top(numbers, operators)` | Pops one operator and two numbers, then pushes the result |
| `evaluate_mathematical_expression(expression)` | Evaluates a single expression string and returns a number |
| `format_result(result)` | Converts `13.0` to `"13"` and leaves real decimals like `2.5` unchanged |
| `is_expression(line)` | Returns `True` if the line contains a digit (otherwise it is a blank or separator line) |
| `read_and_evaluate_file()` | Reads `input.txt`, evaluates every expression line, and returns a list of result strings |
| `write_results_to_file(results)` | Rebuilds the file layout in `output.txt`, inserting results in place of expression lines |
| `main()` | Runs the whole process and prints a summary |

### Design note: how separators are recognised

Rather than matching an exact separator pattern (which breaks if the file uses different underscore characters, tabs, or non-breaking spaces), the program treats **any line without a digit** as a separator or blank line. Every valid expression contains at least one number, so this is a reliable rule.

The file is also opened with `encoding="utf-8-sig"` so that an invisible byte-order mark (BOM) at the start of the file, which some editors such as Windows Notepad add, does not corrupt the first line.

---

## Error Handling

Each line is evaluated independently. A failure on one line does not stop the others; the error message appears in the results and in `output.txt` for that line.

| Situation | Example input | Output |
|---|---|---|
| Division by zero | `5 / 0` | `Error: division by zero` |
| Invalid character | `3 + a` | `Error: Invalid character: a` |
| Missing closing parenthesis | `(2 + 3` | `Error: Mismatched parentheses` |
| Extra closing parenthesis | `2 + 3)` | `Error: Mismatched parentheses` |
| Missing operand | `3 +` | `Error: Malformed expression` |
| Missing operator | `3 4` | `Error: Malformed expression` |

---

## Limitations

- **Unsupported operators:** exponents (`^` or `**`), modulo (`%`), and floor division (`//`) are not supported.
- **No functions or variables:** things like `sqrt(9)` or `x + 2` are not recognised.
- **Unary minus on parentheses:** `-(2 + 3)` is not supported. Write `0 - (2 + 3)` or `(-1) * (2 + 3)` instead. A minus directly before a number (`-3`, `2 * -4`) works.
- **Floating-point precision:** decimals are stored as Python floats, so results like `0.1 + 0.2` display as `0.30000000000000004`.
- **File names are fixed:** the program always reads `input.txt` and writes `output.txt`.
- **A digit in a separator line** (for example `_ _ 1 _`) causes that line to be treated as an expression.
- **Output is overwritten:** each run replaces the previous `output.txt`.

---

## Troubleshooting

**`FileNotFoundError: input.txt`**
The script cannot find the input file. Make sure `input.txt` exists and that you run the command from the folder that contains it. To check which path is being used, add this at the start of `main()`:

```python
import os
print(os.path.abspath("input.txt"))
```

**`Error: Invalid character: _` appears for separator lines**
You are probably running an older version of the code. Replace the entire file with the latest version, save it, and run again. Adding `print("NEW VERSION")` at the top of `main()` is a quick way to confirm which copy is running.

**Results are on the wrong lines**
Results are matched to expression lines in order. Make sure every non-blank, non-separator line in `input.txt` is a single expression.

**Strange characters at the start of the first line**
This is usually a byte-order mark added by some text editors. The program already handles it by using `utf-8-sig`. If you edit the code, keep that encoding.

**Output shows `2.0` instead of `2`**
Make sure results go through `format_result()` before being stored or written.

---

## Possible Improvements

- Accept the input and output file names as command-line arguments (using `argparse`).
- Add support for exponents (`^`), modulo (`%`), and unary minus before parentheses.
- Add support for variables and math functions such as `sqrt` and `abs`.
- Use Python's `decimal` module for exact decimal arithmetic.
- Write unit tests with `unittest` or `pytest` for the evaluator.
- Show line numbers in error messages to make large input files easier to debug.

---

## License

This project is free to use, modify, and share for learning and personal projects.