# Fourmat

A library for batteries-included linting and autoformatting.

## Installation and Usage

Install fourmat through pip:

```sh
$ pip install fourmat
```

Create a `.fourmat` file to specify the directories and files to check.

```sh
$ fourmat check

$ fourmat fix
```

## Adding Fourmat as a pre-commit hook

Install the pre-commit package:

```sh
$ pip install pre-commit
```

Create a `.pre-commit-config.yaml` containing:

```yaml
repos:
- repo: https://github.com/4Catalyzer/fourmat
  rev: master  # or specify a version
  hooks:
    - id: fourmat
```

then install the hook:

```
$ pre-commit install
```
