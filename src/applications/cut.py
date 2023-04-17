from applications.application import application
from applications.decorators import unsafe

from Errors.WrongNumberOfArgsError import WrongNumberOfArgsError
from Errors.InvalidRangeError import InvalidRangeError
from Errors.InvalidFlagsError import InvalidFlagsError
from Errors.NoFileFoundError import NoFileFoundError


class cut(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the cut application

    Refer to /doc/Applications.md
    """

    def __init__(self, args):
        self._app = "cut"
        super().__init__(args)

    def _execute(self):
        output = ""
        if len(self._args) != 2 and len(self._args) != 3:
            raise WrongNumberOfArgsError(
                self._app, "2", "3", str(len(self._args))
            )

        ranges = self._args[1]
        if len(self._args) == 2:
            if self._args[0] != "-b":
                raise InvalidFlagsError(self._app, "-b", self._args[0])
            output = self.__extract_from_stdin(ranges)
            pass

        if len(self._args) == 3:
            if self._args[0] != "-b":
                raise InvalidFlagsError(self._app, "-b", self._args[0])
            file = self._args[2]
            output = self.__extract_from_file(ranges, file)
        return output

    def __ranges_to_set(self, ranges: str, length_of_line):
        s = set()
        for range in ranges.split(","):
            range_components = range.split("-", 1)
            self.__validate_ranges(range_components, range, ranges)
            if len(range_components) == 2:
                if (
                    range_components[0].isnumeric()
                    and range_components[1].isnumeric()
                ):
                    self.__add_numbers_to_set(
                        s,
                        int(range_components[0]) - 1,
                        int(range_components[1]) - 1,
                    )
                if (
                    range_components[0].isnumeric()
                    and range_components[1] == ""
                ):
                    self.__add_numbers_to_set(
                        s, int(range_components[0]) - 1, length_of_line - 1
                    )
                if (
                    range_components[1].isnumeric()
                    and range_components[0] == ""
                ):
                    self.__add_numbers_to_set(
                        s, 0, int(range_components[1]) - 1
                    )

            if len(range_components) == 1:
                if range_components[0].isnumeric():
                    s.add(int(range_components[0]) - 1)
        return s

    def __validate_ranges(self, ranges: list, range: str, arg: str):
        for s in ranges:
            if not s.isnumeric() and not (s == ""):
                raise InvalidRangeError(self._app, range, arg, s)
        pass

    def __add_numbers_to_set(self, s, _from: int, _to: int):
        for i in range(_from, _to + 1):
            s.add(i)
        return 0

    def __extract_from_stdin(self, ranges) -> str:
        output = ""
        inp = ""

        inp = self._stdin
        if not self._stdin_from_file and not self._stdin:
            inp = input()
        tmp = inp.splitlines()

        for line in tmp:
            s = self.__ranges_to_set(ranges, len(line))

            for i in s:
                if i < len(line):
                    output += line[i]

            if not output[len(output) - 1] == "\n":

                output += "\n"
        return output

    def __extract_from_file(self, ranges: str, filename: str) -> str:
        output = ""
        try:
            with open(filename, "rb") as f:
                for line in f:
                    s = self.__ranges_to_set(ranges, len(line))

                    for i in s:
                        output += line[i: i + 1].decode()

                    if not output[len(output) - 1] == "\n":
                        output += "\n"
        except FileNotFoundError:
            raise NoFileFoundError(self._app, filename)
        return output


class _cut(cut):
    @unsafe
    def _execute(self):
        return super()._execute()
