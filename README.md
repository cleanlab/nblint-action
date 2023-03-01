# Notebook Linting GitHub Action

Checks if Jupyter Notebooks in your repository are well formatted according to certain specifications.

## Usage

This GitHub action can conduct a few different types of checks on your notebook, please specify in your inputs which checks should be conducted. 

### General Inputs

| Input | Description | Default |
|-------|-------------|---------|
| `directory` | Directory to search for notebooks. | `"."` | 
| `ignore_paths` | Comma-seperated list of paths to ignore, paths should be relative to the directory specified above. | `""` |

### Inputs Specifying Checks to be Done

| Input | Check Description | Default |
|-------|-------------------|---------|
| `check_outputs_empty` | Check that output cells are empty. | `true` | 
| `check_no_trailing_newline` | Check that there is no newline at the end of code cells. | `true` |
| `check_correct_kernel` | Check that notebook is using the right kernel (here it checks for `Python 3 (ipykernel)`). | `false` | 
| `check_notebook_badge` | Check that notebook has a google colab badge.  | `false` |


## Example Workflow

```yml
name: Sample Workflow
on: push
  
jobs:
  nblint:
    name: Lint Notebooks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: cleanlab/nblint-action@v1
        with:
          directory: 'src'
          ignore_paths: 'path_to_ingore'
          check_outputs_empty: false
          check_correct_kernel: true
```
