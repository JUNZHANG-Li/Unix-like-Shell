import shutil
from applications.application import application
from applications.decorators import unsafe
from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError
from Errors.NoFileFoundError import NoFileFoundError


class mv(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the mkdir application

    Refer to /doc/Applications.md
    """

    def __init__(self, args):
        self._app = "mv"
        super().__init__(args)

    def _execute(self) -> str:
        output = ""
        if len(self._args) != 2:
            raise WrongNumberOfArgsError(self._app, "2", "2", len(self._args))

        src = self._args[0]
        dst = self._args[1]

        try:
            shutil.move(src, dst)
        except FileNotFoundError:
            raise NoFileFoundError(self._app, f"[{src}], [{dst}]")
        return output


class _mv(mv):
    @unsafe
    def _execute(self):
        return super()._execute()
