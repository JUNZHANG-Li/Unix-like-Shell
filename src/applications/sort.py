from applications.application import application
from applications.decorators import unsafe
from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError
from Errors.InvalidFlagsError import InvalidFlagsError
from Errors.NoFileFoundError import NoFileFoundError


class sort(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the sort application

    Refer to /doc/Applications.md
    """
    def __init__(self, args):
        self._app = "sort"
        super().__init__(args)

    def _execute(self):

        if len(self._args) > 2:
            raise WrongNumberOfArgsError(
                self._app, "0", "2", str(len(self._args))
            )
        output = ""
        if len(self._args) == 0:
            output = self.__sort_from_stdin()
        if len(self._args) == 1:
            if self._args[0] == "-r":
                output = self.__sort_from_stdin(reverse=True)
            else:
                output = self.__sort_from_file(self._args[0])
        if len(self._args) == 2:
            if self._args[0] != "-r":
                raise InvalidFlagsError(self._app, "-r", self._args[0])
            output = self.__sort_from_file(self._args[1], reverse=True)
        return output

    def __sort_from_stdin(self, reverse=False) -> str:
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

        tmp.sort()
        if reverse:
            tmp.reverse()
        for line in tmp:
            output += line + "\n"
        return output

    def __sort_from_file(self, filename, reverse=False) -> str:
        """
        Functionality
        -------------
        Helper to self._execute
        """
        output = ""
        lines = list()
        try:
            with open(filename, "r") as f:
                for line in f:
                    lines.append(line)
        except FileNotFoundError:
            raise NoFileFoundError(self._app, filename)
        lines.sort()
        if reverse:
            lines.reverse()
        for line in lines:
            output += line
        return output


class _sort(sort):
    @unsafe
    def _execute(self):
        return super()._execute()
