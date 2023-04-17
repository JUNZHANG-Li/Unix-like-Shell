import re
from applications.application import application
from applications.decorators import unsafe
from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError
from Errors.NoFileFoundError import NoFileFoundError


class grep(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the grep application

    Refer to /doc/Applications.md
    """
    def __init__(self, args):
        self._app = "grep"
        super().__init__(args)

    def _execute(self):
        output = ""
        if len(self._args) < 1:
            raise WrongNumberOfArgsError(
                self._app, "1", "*", str(len(self._args))
            )

        if len(self._args) == 1:
            pattern = self._args[0]
            output = self.__read_lines_from_stdin(pattern)

        if len(self._args) > 1:
            pattern = self._args[0]
            files = self._args[1:]
            output = self.__read_lines_from_file(pattern, files)
        return output

    def __read_lines_from_file(self, pattern: str, files: str) -> str:
        """
        Functionality
        -------------
        Helper to self._execute
        """
        output = ""
        for file in files:
            try:
                with open(file, "r") as f:
                    for line in f:
                        if re.search(pattern, line):
                            if len(files) > 1:
                                output += f"{file}:{line}"
                            else:
                                output += line
            except FileNotFoundError:
                raise NoFileFoundError(self._app, file)
        return output

    def __read_lines_from_stdin(self, pattern: str) -> str:
        """
        Functionality
        -------------
        Helper to self._execute
        """
        output = ""
        inp = ""

        inp = self._stdin
        if not self._stdin_from_file and not self._stdin:
            inp = input()
        tmp = inp.splitlines()

        for line in tmp:
            if re.search(pattern, line):
                output += line + "\n"
        return output


class _grep(grep):
    @unsafe
    def _execute(self):
        return super()._execute()
