# Black8

A library for batteries-included linting and autoformatting.

## Usage

Install black8 through pip:

```sh
$ pip install black8
```

Create a `.black8` file to specify the directories and files to check.

## Adding Black8 as a pre-commit hook

Install the pre-commit package:

```sh
$ pip install pre-commit
```

Create a `.pre-commit-config.yaml` containing:

```yaml
repos:
- repo: local
  hooks:
    - id: black8
      name: black8
      entry: black8 format
      language: system
      types: [python]
```

then install the hook:

```
$ pre-commit install
```
