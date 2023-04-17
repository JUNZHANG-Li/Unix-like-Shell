import os
from applications.application import application
from applications.decorators import unsafe
from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError


class mkdir(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the mkdir application

    Refer to /doc/Applications.md
    """

    def __init__(self, args):
        self._app = "mkdir"
        super().__init__(args)

    def _execute(self) -> str:
        output = ""
        if len(self._args) != 1:
            raise WrongNumberOfArgsError(self._app, "1", "1", len(self._args))

        dir = self._args[0]
        if not os.path.exists(dir):
            os.mkdir(dir)
        return output


class _mkdir(mkdir):
    @unsafe
    def _execute(self):
        return super()._execute()
