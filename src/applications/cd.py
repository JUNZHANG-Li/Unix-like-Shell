from applications.application import application
from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError
from Errors.DirectoryNotFoundError import DirectoryNotFoundError
from applications.decorators import unsafe

import os


class cd(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the cd application

    Refer to /doc/Applications.md
    """

    def __init__(self, args):
        self._app = "cd"
        super().__init__(args)

    def _execute(self):
        output = ""
        if len(self._args) != 1:
            raise WrongNumberOfArgsError(
                self._app, "1", "1", str(len(self._args))
            )

        try:
            os.chdir(self._args[0])
        except FileNotFoundError:
            raise DirectoryNotFoundError(self._app, self._args[0])

        return output


class _cd(cd):
    @unsafe
    def _execute(self):
        return super()._execute()
