# Difference Calculator

# Hexlet tests and linter status:
[![Actions Status](https://github.com/blizneci/python-project-50/workflows/hexlet-check/badge.svg)](https://github.com/blizneci/python-project-50/actions) [![Maintainability](https://api.codeclimate.com/v1/badges/c324c2fd290ab3649de0/maintainability)](https://codeclimate.com/github/blizneci/python-project-50/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/c324c2fd290ab3649de0/test_coverage)](https://codeclimate.com/github/blizneci/python-project-50/test_coverage)

## About this project

This is a cli utility for calculating differences between two configuration files.
It works with JSON and YAML/YML plain and deep nested files.
It has three output formats: "stylish" (default formatter), "plain", "json".
"stylish" and "plain" formats have colored output.

## Installation

Use python3.11 or higher and package manager [poetry1.2.0](https://python-poetry.org/docs/)
or higher to install dependencies, build and install package.

Clone this repository to your computer:
```bash
git clone https://github.com/blizneci/python-project-50.git
```
Or with GitHub CLI:
```bash
gh repo clone blizneci/python-project-50
```
Move into the project directory 
```bash
cd python-project-50
```
Use commands:
- ```make install``` to install dependencies
- ```make build``` to build the project
- ```make package-install``` to install the utility

## Usage

Use `gendiff --help` for details.
Default usage is:
```bash
gendiff file1.json file2.json
```

## Demonstrations

#### Gendiff with Stylish formatter for plain/nested files.
[![asciicast](https://asciinema.org/a/8nDbKZf8sqe6DUopXZhoOpqeW.svg)](https://asciinema.org/a/8nDbKZf8sqe6DUopXZhoOpqeW)

#### Gendiff with Plain formatter for plain/nested files.
[![asciicast](https://asciinema.org/a/9nnTdF8CYnjd2sDYFK2JUlaUi.svg)](https://asciinema.org/a/9nnTdF8CYnjd2sDYFK2JUlaUi)

#### Gendiff with JSON formatter for plain/nested files.
[![asciicast](https://asciinema.org/a/asMoMsrErA27mgzpghuHZyRRZ.svg)](https://asciinema.org/a/asMoMsrErA27mgzpghuHZyRRZ)
