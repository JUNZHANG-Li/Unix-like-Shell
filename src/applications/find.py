from applications.application import application
from applications.decorators import unsafe
from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError
from Errors.InvalidFlagsError import InvalidFlagsError
from pathlib import Path
import os


class find(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the find application

    Refer to /doc/Applications.md
    """
    def __init__(self, args):
        self._app = "find"
        super().__init__(args)

    def _execute(self):
        output = ""
        path = ""
        pattern = ""
        if len(self._args) != 2 and len(self._args) != 3:
            raise WrongNumberOfArgsError(
                self._app, "2", "3", str(len(self._args))
            )

        if len(self._args) == 2:
            if self._args[0] != "-name":
                raise InvalidFlagsError(self._app, "-name", self._args[0])
            path = "." + os.sep
            pattern = self._args[1]

        if len(self._args) == 3:
            if self._args[1] != "-name":
                raise InvalidFlagsError(self._app, "-name", self._args[1])

            path = self._args[0]
            if not path[-1] == os.sep:
                path += os.sep
            pattern = self._args[2]

        for P in Path(path).rglob(pattern):
            output += path + str(P.relative_to(path)) + "\t"
        output = output[: len(output) - 1] + "\n"
        return output


class _find(find):
    @unsafe
    def _execute(self):
        return super()._execute()
