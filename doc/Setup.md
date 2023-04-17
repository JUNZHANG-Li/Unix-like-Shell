# COMP0010 Shell (Setup)

To use the COMP0010 Shell, first [build the shell](#build-the-shell) then [execute the shell](#execute-the-shell) by running the command of choice.

# Catalogue

### Shell (COMP0010)
 - [Build the Shell](#build-the-shell)
 - [Execute the Shell](#execute-the-shell)
 - [Unit Tests](#unit-tests)
 - [Code Analysis](#code-analysis)
 - [Test Coverage](#test-coverage)
 - [System Test](#system-test)

### Parser (ANTLR4)
 - [Abstract Syntax Tree](#abstract-syntax-tree)

## Build the Shell

This Shell can be executed in a Docker container. To build a container image (let's call it `shell`), run

    docker build -t shell .

## Execute the Shell

To execute the shell in interactive mode, build the shell first, and run

    docker run -it --rm shell /comp0010/sh

To execute the shell in non-interactive mode (to evaluate a specific command such as `echo foo`), build the shell first, and run

    docker run --rm shell /comp0010/sh -c 'echo foo'

## Unit Tests

To execute unit tests, build the shell first, and run

    docker run -p 80:8000 -ti --rm shell /comp0010/tools/test

Then, the results of unit testing will be available at [http://localhost](http://localhost)

## Code Analysis

To execute code analysis, build the shell first, and run

    docker run -p 80:8000 -ti --rm shell /comp0010/tools/analysis

Then, the results of code analysis will be available at [http://localhost](http://localhost)

## Test Coverage

To execute test coverage, build the shell first, and run

    docker run -p 80:8000 -ti --rm shell /comp0010/tools/coverage

Then, the results of coverage computation will be available at [http://localhost](http://localhost)

## System Test

To execute system tests, build the shell first, and build a Docker image named `comp0010-system-test`:

    docker build -t comp0010-system-test .

Then, execute system tests using the following command (Python 3.7 or higher is required):

    python system_test/tests.py -v

Individual system tests (e.g. `test_cat`) can be executed as

    python system_test/tests.py -v TestShell.test_cat

### Implementation of Parser(ANTLR4)
## Abstract Syntax Tree

To generate a diagram of the Abstract Syntax Tree of any command, change directory to /src/command_parser/Grammar, and run

    antlr4-parse command.g4 command -gui

Then type in the command as prompted, and pressing `CTRL+D` (Linux & Mac) / `CTRL+Z` (Windons) followed by `Enter`
