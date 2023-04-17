from applications.application import application
from applications.decorators import unsafe

from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError
from Errors.InvalidFlagsError import InvalidFlagsError
from Errors.NoFileFoundError import NoFileFoundError


class uniq(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the uniq application

    Refer to /doc/Applications.md
    """

    def __init__(self, args):
        self._app = "uniq"
        super().__init__(args)

    def _execute(self):

        output = ""
        if len(self._args) > 2:
            raise WrongNumberOfArgsError(
                self._app, "0", "2", str(len(self._args))
            )

        if len(self._args) == 0:
            output = self.__uniq_from_stdin(case_sensitive=True)
            pass
        if len(self._args) == 1:
            if self._args[0] == "-i":
                output = self.__uniq_from_stdin()
            else:
                output = self.__uniq_from_file(
                    self._args[0], case_sensitive=True
                )
        if len(self._args) == 2:
            if self._args[0] != "-i":
                raise InvalidFlagsError(self._app, "-i", self._args[0])
            output = self.__uniq_from_file(self._args[1])

        return output

    def __uniq_from_stdin(self, case_sensitive: bool = False):
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

        previous_line = ""
        for line in tmp:
            if not self.__match(previous_line, line, case_sensitive):
                output += line + "\n"
                previous_line = line

        return output

    def __uniq_from_file(self, filename, case_sensitive: bool = False):
        """
        Functionality
        -------------
        Helper to self._execute
        """
        output = ""
        previous_line = ""
        try:
            with open(filename, "r") as f:
                for line in f:
                    if not self.__match(previous_line, line, case_sensitive):
                        output += line
                        previous_line = line
        except FileNotFoundError:
            raise NoFileFoundError(self._app, filename)

        return output

    def __match(self, line1, line2, case_sensitive: bool = False):
        """
        Functionality
        -------------
        Helper to self.__uniq_from_file and __uniq_from_stdin
        """
        if len(line1) != len(line2):
            return False
        if case_sensitive:
            for i in range(len(line1)):
                if line1[i] != line2[i]:
                    return False
        if not case_sensitive:
            for i in range(len(line1)):
                if line1[i].lower() != line2[i].lower():
                    return False
        return True


class _uniq(uniq):
    @unsafe
    def _execute(self):
        return super()._execute()
