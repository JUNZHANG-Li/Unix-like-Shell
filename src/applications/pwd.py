import os
from applications.application import application
from applications.decorators import unsafe

from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError


class pwd(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the pwd application

    Refer to /doc/Applications.md
    """
    def __init__(self, args):
        self._app = "pwd"
        super().__init__(args)

    def _execute(self):
        if len(self._args) != 0:
            raise WrongNumberOfArgsError(
                self._app, "0", "0", str(len(self._args))
            )
        output = os.getcwd() + "\n"
        return output


class _pwd(pwd):
    @unsafe
    def _execute(self):
        return super()._execute()
