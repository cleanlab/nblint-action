#!/usr/bin/env python

import json
import os
import sys


def main():
    dir = os.environ["INPUT_DIRECTORY"]
    notebooks = find_notebooks(dir)

    checks = []
    if os.environ["INPUT_CHECK_OUTPUTS_EMPTY"] == "true":
        checks.append(check_outputs_empty)
    if os.environ["INPUT_CHECK_NO_TRAILING_NEWLINE"] == "true":
        checks.append(check_no_trailing_newline)
    if os.environ["INPUT_CHECK_CORRECT_KERNEL"] == "true":
        checks.append(check_correct_kernel)
    if os.environ["INPUT_CHECK_NOTEBOOK_BADGE"] == "true":
        checks.append(check_notebook_badge)
    for notebook in notebooks:
        check(notebook, checks)


def find_notebooks(dir):
    notebooks = set()
    for dirname, _, filenames in os.walk(dir):
        for filename in filenames:
            if not filename.endswith(".ipynb"):
                continue
            full_path = os.path.join(dirname, filename)
            notebooks.add(full_path)
    return notebooks


def check(notebook, checks):
    with open(notebook) as f:
        contents = json.load(f)
    for c in checks:
        c(notebook, contents)
    print(f"{notebook}: OK")


def check_outputs_empty(path, contents):
    for i, cell in enumerate(contents["cells"]):
        if "outputs" in cell and cell["outputs"] != []:
            fail(path, "output is not empty", i)


def check_no_trailing_newline(path, contents):
    """
    Checks that the last line of a code cell doesn't end with a newline, which
    produces an unnecessarily newline in the doc rendering.
    """
    for i, cell in enumerate(contents["cells"]):
        if cell["cell_type"] != "code":
            continue
        if "source" not in cell or len(cell["source"]) == 0:
            fail(path, "code cell is empty", i)
        if cell["source"][-1].endswith("\n"):
            fail(path, "unnecessary trailing newline", i)


def check_correct_kernel(path, contents):
    if contents["metadata"]["kernelspec"]["display_name"] != "Python 3 (ipykernel)":
        fail(path, "kernel is incorrect")


def check_notebook_badge(path, contents):
    first_cell = contents["cells"][1]["source"][0]
    if not ("<!--<badge>-->" in first_cell or "{{ badge }}" in first_cell):
        fail(path, "missing colab badge")


def fail(path, message, cell=None):
    cell_msg = f" [cell {cell}]" if cell is not None else ""
    print(f"{path}{cell_msg}: {message}")
    sys.exit(1)


if __name__ == "__main__":
    main()
