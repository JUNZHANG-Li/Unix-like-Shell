import sys
import os
import readline
from collections import deque
from sub_shell import sub_shell
from Features.Command_Substituter import Command_Substituter
from Features.Quote_Remover import Quote_Remover
from Features.Globber import Globber
from Features.Application_Setter import Application_Setter
from Errors.InvalidCommandError import InvalidCommandError


class shell(sub_shell):
    """
    <Class>
    ----------------

    Purpose
    -------
    Main component of shell
    """

    def eval(self, cmdline: str, stdOut: deque):
        super().__init__(cmdline, stdOut)

        try:
            self.parse()
        except InvalidCommandError as ic:
            print(ic, file=sys.stderr)
            exit()

        self._call_glober(Globber(), self)
        self._call_quote_remover(Quote_Remover(), self)
        self._call_command_substituter(Command_Substituter(), self, shell())
        self._call_application_setter(Application_Setter(), self)
        self.execute()

        return 0


def prompt_with_history_autocomplete(prompt):  # pragma: no cover
    def hook():
        readline.parse_and_bind("tab: complete")

        def auto_complete(text, state):
            result = deque()
            shell().eval("ls -a", result)
            dir = result.popleft()
            volcab = dir.replace("\n", "").split("\t")
            results = [x for x in volcab if x.startswith(text)]
            return results[state]

        readline.set_completer(auto_complete)
        readline.redisplay()

    readline.set_pre_input_hook(hook)
    result = input(prompt)
    return result


if __name__ == "__main__":  # pragma: no cover
    args_num = len(sys.argv) - 1
    if args_num > 0:
        if args_num != 2:
            raise ValueError("wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        out = deque()
        shell().eval(sys.argv[2], out)
        while len(out) > 0:
            print(out.popleft(), end="")
    else:
        while True:
            # print(os.getcwd() + "> ", end="")
            cmdline = prompt_with_history_autocomplete(os.getcwd() + "> ")
            out = deque()
            shell().eval(cmdline, out)
            while len(out) > 0:
                print(out.popleft(), end="")
