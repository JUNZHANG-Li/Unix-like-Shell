from applications.application import application
from applications.decorators import unsafe


class echo(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the echo application
    """
    def __init__(self, args) -> None:
        self._app = "echo"
        super().__init__(args)

    def _execute(self):
        output = ""
        output = " ".join(self._args) + "\n"
        return output


class _echo(echo):
    @unsafe
    def _execute(self):
        return super()._execute()
