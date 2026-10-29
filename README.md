# goit-pycore-hw-04

Homework 4 — working with files, the filesystem, command-line arguments, and a console assistant bot.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .
```

`pip install -e .` makes the `hw04` package importable, which both the tests and the
`python -m hw04.<package>` commands rely on.
For runtime dependencies only, use `pip install -r requirements.txt`.

## Project layout

Each task lives in its own package under `src/hw04/`, and the tests mirror that structure.

```
files/                      sample data (salary_file.txt, cats_file.txt)
src/hw04/
    task1/salary.py         total and average salary
    task2/cats.py           cat records
    task3/directory_tree.py coloured directory tree (CLI)
    chatbot/                console assistant bot (CLI)
        main.py             command loop
        data.py             input parsing
        commands/           one module per command
tests/
    task1/  task2/  chatbot/
```

---

## Task 1 — total and average salary

[src/hw04/task1/salary.py](src/hw04/task1/salary.py)

Reads a text file where each line is `name,salary` and returns a tuple of the total payroll and the average salary.

```python
from hw04.task1 import total_salary

total, average = total_salary("files/salary_file.txt")
# (6000, 2000.0)
```

Input format — [files/salary_file.txt](files/salary_file.txt):

```
Alex Korp,3000
Nikita Borisenko,2000
Sitarama Raju,1000
```

Behaviour:

- Blank lines are skipped; whitespace around fields is trimmed.
- Exactly two comma-separated fields are required, so a name containing a comma is rejected.
- An empty file returns `(0, 0)`.
- A missing file raises `FileNotFoundError`.
- Malformed input raises `ValueError` naming the offending line number: wrong field count, empty name, non-numeric salary, or negative salary.

---

## Task 2 — cat records

[src/hw04/task2/cats.py](src/hw04/task2/cats.py)

Reads a text file where each line is `id,name,age` and returns a list of dictionaries.

```python
from hw04.task2 import get_cats_info

cats = get_cats_info("files/cats_file.txt")
# [{"id": "60b90c1c13067a15887e1ae1", "name": "Tayson", "age": 3}, ...]
```

Input format — [files/cats_file.txt](files/cats_file.txt):

```
60b90c1c13067a15887e1ae1,Tayson,3
60b90c2413067a15887e1ae2,Vasya,2
60b90c2e13067a15887e1ae3,Barsik,1
```

Behaviour:

- `id` and `name` stay strings; `age` is converted to `int`.
- File order is preserved. Blank lines are skipped, fields are trimmed.
- An empty file returns `[]`.
- A missing file raises `FileNotFoundError`.
- Exactly three fields are required, so commas inside a name are rejected.
- Malformed input raises `ValueError` with the line number: wrong field count, empty id/name/age, non-numeric age, or negative age.

---

## Task 3 — coloured directory tree

[src/hw04/task3/directory_tree.py](src/hw04/task3/directory_tree.py)

Takes a directory path as a command-line argument (via `sys.argv`) and prints its contents recursively. Directories are shown in bright blue with a trailing `/`, files in green. Each nesting level is indented by two spaces, and entries are sorted for stable output.

Run:

```bash
python -m hw04.task3 files
python -m hw04.task3 /absolute/path/to/directory
python -m hw04.task3 "folder with spaces"
```

Without an argument it prints a usage message and exits with code `1`.

Requires `colorama`.

---

## Task 4 — console assistant bot

[src/hw04/chatbot/main.py](src/hw04/chatbot/main.py)

An interactive bot that keeps contacts in memory for the duration of the session. Input is lowercased and split into a command plus arguments by [data.py](src/hw04/chatbot/data.py); each command is a separate module under [commands/](src/hw04/chatbot/commands).

Run:

```bash
python -m hw04.chatbot
```

Commands:

| Command | Description |
|---|---|
| `hello` | greet the bot |
| `add <name> <phone>` | add a new contact |
| `change <name> <phone>` | update an existing contact |
| `show <name>` | show the phone number of a contact |
| `all` | list all contacts |
| `close` / `exit` | quit the assistant |

The list is printed automatically after the welcome message. Names are case-sensitive, and contacts are not persisted between runs.

---

## Tests

```bash
pytest                              # everything
pytest tests/task1 -q               # one task
pytest tests/chatbot -q             # the bot commands
pytest -v                           # per-test names
```

Tests write their fixtures into a temporary directory, so the files in `files/` are never modified.
