from applications.application import application

from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError
from Errors.DirectoryNotFoundError import DirectoryNotFoundError
from applications.decorators import unsafe
import os


class ls(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the ls application

    Refer to /doc/Applications.md
    """

    def __init__(self, args):
        self._app = "ls"
        super().__init__(args)

    def _execute(self):
        if len(self._args) > 1:
            raise WrongNumberOfArgsError(
                self._app, "0", "1", str(len(self._args))
            )
        if len(self._args) == 0 or (
            len(self._args) == 1 and self._args[0] == "-a"
        ):
            ls_dir = os.getcwd()
        else:
            ls_dir = self._args[0]

        output = ""

        try:
            for f in os.listdir(ls_dir):
                if not f.startswith("."):
                    output += f + "\t"
            output = output[:-1] + "\n"
        except FileNotFoundError:
            raise DirectoryNotFoundError(self._app, ls_dir)

        return output


class _ls(ls):
    @unsafe
    def _execute(self):
        return super()._execute()
