from applications.application import application
from Errors.NoFileFoundError import NoFileFoundError

from applications.decorators import unsafe


class cat(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the cat application

    Refer to /doc/Applications.md
    """

    def __init__(self, args):
        self._app = "cat"
        super().__init__(args)

    def _execute(self):
        if not self._args:
            output = self._stdin
            if not self._stdin_from_file and not self._stdin:
                output = input()
            return output

        output = ""
        for arg in self._args:
            try:
                with open(arg, "r") as f:
                    output += f.read()
            except FileNotFoundError:
                raise NoFileFoundError(self._app, arg)
        return output


class _cat(cat):
    @unsafe
    def _execute(self):
        return super()._execute()
