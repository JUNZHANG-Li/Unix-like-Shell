from command.Command import Command
from command.Call import Call
from command.Pipe import Pipe
from sub_shell import sub_shell
from Features.Feature import Feature
from collections import deque
import glob


class Globber(Feature):
    """
    <Class>
    -------

    Purpose
    -------
    To globe all unquoted asterisks (*) in arguments in command
    """

    def __init__(self) -> None:
        pass

    def globe(self, ss: sub_shell) -> int:
        """
        Functionality
        -------------
        To globe all unquoted astericks of command in subshell
        """
        for command in ss.getCommandSequence():
            self.__globe(command)
        return 0

    def __globe(self, cmd: Command):
        """
        Functionality
        -------------
        To globe unquoted astericks of argument
        terminals of subcommands in subshell
        """
        if isinstance(cmd, Call):
            self.__globe_args(cmd)

        if isinstance(cmd, Pipe):
            for call in cmd.getCalls():
                self.__globe_args(call)

    def __globe_args(self, cmd: Call) -> int:
        """
        Functionality
        -------------
        Helper for __globe
        """
        args = cmd.getArgs()

        # if args is None:
        #     return 0

        for i in range(len(args)):
            if self.__has_unquoted_asterisks(args[i]):
                globbed = glob.glob(args[i])
                if len(globbed) != 0:
                    self._replace_arg_with_args(args, i, globbed)

        return 0

    def __has_unquoted_asterisks(self, arg: str):
        """
        Functionality
        -------------
        Helper for __glove_args: To check if
        an argument terminal has unquoted_astrisks
        """
        quote = deque()
        for i in range(len(arg)):
            if len(quote) != 0 and arg[i] == quote[0]:
                quote.popleft()
            elif arg[i] in {"'", '"', "`"}:
                quote.append(arg[i])

            if len(quote) == 0 and arg[i] == "*":
                return True
        return False
