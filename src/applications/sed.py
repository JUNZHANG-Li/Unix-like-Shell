import re
from applications.application import application
from applications.decorators import unsafe
from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError
from Errors.InvalidFormatError import InvalidFormatError
from Errors.NoFileFoundError import NoFileFoundError


class sed(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the sed application

    Refer to /doc/Applications.md
    """

    def __init__(self, args):
        self._app = "sed"
        super().__init__(args)

    def _execute(self) -> str:
        output = ""
        if len(self._args) != 1 and len(self._args) != 2:
            raise WrongNumberOfArgsError(self._app, "1", "2", len(self._args))

        sed_delimiter = self.sed_delimiter(self._args[0])
        sed_args = [x for x in self._args[0].split(sed_delimiter) if x]
        if len(self._args) == 1:
            output = self.sed_from_stdin(sed_args)
        if len(self._args) == 2:
            output = self.sed_from_file(sed_args)

        return output

    def sed_delimiter(self, arg):
        if "|" in arg and "/" in arg:
            raise ValueError("Inconsistent delimiter used")
        if "|" in arg:
            return "|"
        if "/" in arg:
            return "/"

    def sed_from_file(self, sed_args):
        output = ""
        filename = self._args[1]
        try:
            with open(filename, "r") as f:
                if (
                    len(sed_args) == 4
                    and sed_args[0] == "s"
                    and sed_args[3] == "g"
                ):
                    for line in f:
                        replaced_line = re.sub(sed_args[1], sed_args[2], line)
                        output += replaced_line
                elif len(sed_args) == 3 and sed_args[0] == "s":
                    for line in f:
                        replaced_line = re.sub(
                            sed_args[1], sed_args[2], line, 1
                        )
                        output += replaced_line
                else:
                    raise InvalidFormatError(
                        self._app, '"s/regexp/replacement/g"', self._args[0]
                    )
        except FileNotFoundError:
            raise NoFileFoundError(self._app, filename)

        return output

    def sed_from_stdin(self, sed_args):
        output = ""

        inp = self._stdin
        if not self._stdin_from_file and not self._stdin:
            inp = input()
        tmp = inp.splitlines()

        if len(sed_args) == 4 and sed_args[0] == "s" and sed_args[3] == "g":
            for line in tmp:
                replaced_line = re.sub(sed_args[1], sed_args[2], line)
                output += replaced_line + "\n"
        elif len(sed_args) == 3 and sed_args[0] == "s":
            for line in tmp:
                replaced_line = re.sub(sed_args[1], sed_args[2], line, 1)
                output += replaced_line + "\n"
        else:
            raise InvalidFormatError(
                self._app, '"s/regexp/replacement/g"', self._args[0]
            )

        return output


class _sed(sed):
    @unsafe
    def _execute(self):
        return super()._execute()
