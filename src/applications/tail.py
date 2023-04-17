from applications.application import application
from applications.decorators import unsafe

from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError
from Errors.InvalidFlagsError import InvalidFlagsError
from Errors.NotANumberError import NotANumberError
from Errors.NoFileFoundError import NoFileFoundError


class tail(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the tail application

    Refer to /doc/Applications.md
    """
    def __init__(self, args):
        self._app = "tail"
        super().__init__(args)

    def _execute(self):

        output = ""
        if len(self._args) > 3:
            raise WrongNumberOfArgsError(
                self._app, "0", "3", str(len(self._args))
            )

        if len(self._args) == 0:
            num_lines = 10
            output = self.__read_lines_from_stdin(num_lines)
        if len(self._args) == 1:
            num_lines = 10
            file = self._args[0]
            output = self.__read_lines_from_file(file, num_lines)
        if len(self._args) == 2:
            self.__validate_args()
            output = self.__read_lines_from_stdin(int(self._args[1]))
        if len(self._args) == 3:
            self.__validate_args()
            num_lines = int(self._args[1])
            file = self._args[2]
            output = self.__read_lines_from_file(file, num_lines)
        return output

    def __validate_args(self):
        """
        Functionality
        -------------
        Helper to self._execute
        """
        if self._args[0] != "-n":
            raise InvalidFlagsError(self._app, "-n", self._args[0])
        if not self._args[1].isnumeric():
            raise NotANumberError(self._app, "2", self._args, self._args[1])

    def __read_lines_from_file(self, filename: str, num_lines: int) -> str:
        """
        Functionality
        -------------
        Helper to self._execute
        """
        output = ""
        try:
            with open(filename) as f:
                lines = f.readlines()
                display_length = min(len(lines), num_lines)
                for i in range(0, display_length):
                    output += lines[len(lines) - display_length + i]
        except FileNotFoundError:
            raise NoFileFoundError(self._app, filename)
        return output

    def __read_lines_from_stdin(self, num_lines: int) -> str:
        """
        Functionality
        -------------
        Helper to self._execute
        """
        output = ""
        if num_lines == 0:
            return output
        inp = ""

        inp = self._stdin
        if not self._stdin_from_file and not self._stdin:
            inp = input()
        tmp = inp.splitlines()

        display_length = min(len(tmp), num_lines)
        for i in range(0, display_length):
            output += (tmp[len(tmp) - display_length + i]) + "\n"
        return output


class _tail(tail):
    @unsafe
    def _execute(self):
        return super()._execute()
