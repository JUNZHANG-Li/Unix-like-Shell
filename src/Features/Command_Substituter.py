from sub_shell import sub_shell
from command.Command import Command
from command.Call import Call
from command.Pipe import Pipe
from collections import deque
from Features.Feature import Feature
import re


class Command_Substituter(Feature):
    """
    <Class>
    -------

    Purpose
    -------
    To command substitute any backquotes in the current executing command
    """

    def __init__(self) -> None:
        pass

    def command_substitute(self, ss: sub_shell, new_shell: sub_shell) -> int:
        """
        Functionality
        -------------
        To substitute the command running in the
        current running subshell with a new instance
        of sub_shell

        Parameters
        ----------
        ss : sub_shell
            the current running instance of sub shell
        new_shell : sub_shell
            a new instance of sub_shell for command substitution

        Returns
        -------
        Literal[0] : int
            Exit Status
        """
        for command in ss.getCommandSequence():
            self.__substitute(command, new_shell)
        return 0

    def __substitute(self, cmd: Command, new_shell):
        """
        Functionality
        -------------
        Helper function for command_substitute
        """
        if isinstance(cmd, Call):
            self.__substitute_args(cmd, new_shell)

        if isinstance(cmd, Pipe):
            for call in cmd.getCalls():
                self.__substitute_args(call, new_shell)

    def __substitute_args(self, call: Call, new_shell: sub_shell):
        """
        Functionality
        -------------
        Helper function for __substitute
        """
        shell_stdout = deque()
        args = call.getArgs()

        for i in range(len(args)):
            if self.__is_surrounded_backquote(args[i]):
                splitted_args = args[i].split("`")
                replacement_arg = ""
                for j in range(0, len(splitted_args)):
                    if j % 2 == 0:
                        replacement_arg += splitted_args[j]
                    else:
                        command_to_exeute = splitted_args[j]
                        s = new_shell
                        s.eval(command_to_exeute, shell_stdout)

                        replacement_arg += self.__get_shell_stdout_as_string(
                            shell_stdout
                        )
                self.__replace_arg(
                    args,
                    i,
                    self.__replace_whitespaces_with_space(
                        self.__remove_all_newlines(replacement_arg)
                    ),
                )

    def __is_surrounded_backquote(self, arg: str):
        """
        Functionality
        -------------
        Helper function for __substitute_args
        """
        if re.compile("[^`^']*(`.+`)[^`^']*").match(arg) is not None:
            return True
        return False

    def __replace_arg(self, args: list, index_in_args: int, stdout: str):
        """
        Functionality
        -------------
        Helper function for __substitute_args
        """
        splitted_by_whitespace = [arg for arg in stdout.split(" ") if arg]
        args_from_stdout = list()
        for i in range(len(splitted_by_whitespace)):
            if (
                len(args_from_stdout) > 0
                and args_from_stdout[len(args_from_stdout) - 1].count('"') % 2
                != 0
            ):
                args_from_stdout[len(args_from_stdout) - 1] = (
                    args_from_stdout[len(args_from_stdout) - 1]
                    + " "
                    + splitted_by_whitespace[i]
                )
            else:
                args_from_stdout.append(splitted_by_whitespace[i])

        self._replace_arg_with_args(args, index_in_args, args_from_stdout)

    """Helper functions"""

    def __get_shell_stdout_as_string(self, stdout: deque):
        """
        Functionality
        -------------
        Helper function
        """
        s = ""
        while len(stdout) != 0:
            s += stdout.popleft()
        return s

    def __remove_all_newlines(self, s: str):
        """
        Functionality
        -------------
        Helper function
        """
        return self.__replace_unix_newline_with_space(
            self.__replace_wins_newline_with_space(s)
        )

    def __replace_unix_newline_with_space(self, s: str):
        """
        Functionality
        -------------
        Helper function
        """
        return s.replace("\n", "")

    def __replace_wins_newline_with_space(self, s: str):
        """
        Functionality
        -------------
        Helper function
        """
        return s.replace("\r\n", "")

    def __replace_whitespaces_with_space(self, s: str):
        """
        Functionality
        -------------
        Helper function
        """
        return " ".join(s.split())
