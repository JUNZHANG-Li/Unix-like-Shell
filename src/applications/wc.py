from applications.application import application
from applications.decorators import unsafe
from Errors.NoFileFoundError import NoFileFoundError


class wc(application):
    """
    <class>
    -------

    Purpose
    -------
    Implements the functionalities of the wc application

    Refer to /doc/Applications.md
    """

    def __init__(self, args):
        self._app = "wc"
        super().__init__(args)

    def _execute(self) -> str:
        valid_flags = {"-l", "-m", "-w"}
        output = ""

        if len(self._args) == 0:
            output = self.wc_from_stdin("-all")
        if len(self._args) == 1 and self._args[0] in valid_flags:
            flag = self._args[0]
            output = self.wc_from_stdin(flag)
        if len(self._args) >= 1 and not self._args[0] in valid_flags:
            output = self.wc_from_file("-all", self._args)
        if len(self._args) > 1 and self._args[0] in valid_flags:
            flag = self._args[0]
            files = self._args[1:]
            output = self.wc_from_file(flag, files)

        if output[-1] != "\n":
            output = output + "\n"

        return output

    def wc_from_file(self, flag, files):
        output = ""
        line_count = 0
        if flag == "-l":
            for filename in files:
                try:
                    with open(filename, "r") as f:
                        line_count += self.count_lines(f.read())
                except FileNotFoundError:
                    raise NoFileFoundError(self._app, filename)
            output = str(line_count)

        if flag == "-m":
            char_count = 0
            for filename in files:
                try:
                    with open(filename, "r") as f:
                        char_count += self.count_chars(f.read())
                except FileNotFoundError:
                    raise NoFileFoundError(self._app, filename)
            output = str(char_count)

        if flag == "-w":
            word_count = 0
            for filename in files:
                try:
                    with open(filename, "r") as f:
                        word_count += self.count_words(f.read())
                except FileNotFoundError:
                    raise NoFileFoundError(self._app, filename)
            output = str(word_count)

        if flag == "-all":
            for filename in files:
                try:
                    with open(filename, "r") as f:
                        inp = f.read()
                        if len(files) == 1:
                            output += (
                                str(self.count_lines(inp))
                                + "\t"
                                + str(self.count_words(inp))
                                + "\t"
                                + str(self.count_chars(inp))
                            )
                        else:
                            output += (
                                str(self.count_lines(inp))
                                + "\t"
                                + str(self.count_words(inp))
                                + "\t"
                                + str(self.count_chars(inp))
                                + "\t"
                                + filename
                                + "\n"
                            )
                except FileNotFoundError:
                    raise NoFileFoundError(self._app, filename)
        return output

    def wc_from_stdin(self, flag):
        output = ""

        inp = self._stdin
        if not self._stdin_from_file and not self._stdin:
            inp = input()

        if flag == "-l":
            output = str(self.count_lines(inp))
        if flag == "-m":
            output = str(self.count_chars(inp))
        if flag == "-w":
            output = str(self.count_words(inp))
        if flag == "-all":
            output += (
                str(self.count_lines(inp))
                + "\t"
                + str(self.count_words(inp))
                + "\t"
                + str(self.count_chars(inp))
            )

        return output

    def count_words(self, inp):
        word_count = 0
        for c in [
            x
            for x in inp.replace("\n", " ").replace("\t", " ").split(" ")
            if x
        ]:
            word_count += 1
        return word_count

    def count_chars(self, inp):
        char_count = 0
        for c in inp:
            char_count += 1
        return char_count

    def count_lines(self, inp):
        line_count = 0
        for line in inp.splitlines():
            line_count += 1
        return line_count


class _wc(wc):
    @unsafe
    def _execute(self):
        return super()._execute()
