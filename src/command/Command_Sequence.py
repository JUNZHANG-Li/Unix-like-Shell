from command.Call import Call
from command.Pipe import Pipe
from parser import Parser
from antlr4.error.Errors import ParseCancellationException
from Errors.InvalidCommandError import InvalidCommandError
from collections import deque


class Command_Sequence:
    def __init__(self, cmd_line="", stdout=deque()) -> None:
        self._shell_stdOut = stdout
        self._cmdline = cmd_line
        self._command_sequence = deque()
        self._sequence_order = deque()
        self.__parse()

    def __parse(self):
        """
        Functionality
        -------------
        Parses the current command being run into
        Call subcommand and Pipe subcommand
        """
        try:
            p = Parser()
            p.parse(self._cmdline)
            commands_tokens = p.getTokens()
            self._sequence_order = p.getSequenceOrder()
        except ParseCancellationException:
            raise InvalidCommandError(self._cmdline) from None

        self._cmdline = self.__replace_unquoted_double_ops_with_semicolon(
            self._cmdline
        )

        commands = list()
        self.__parse_semicolon_command(self._cmdline, commands)

        for current_command in range(len(commands_tokens)):
            cmd_tokens = commands_tokens[current_command]
            cmd_str = commands[current_command]

            if self.__hasPipe(cmd_tokens):
                self._command_sequence.append(Pipe(cmd_tokens, cmd_str))
            if not self.__hasPipe(cmd_tokens):
                self._command_sequence.append(Call(cmd_tokens, cmd_str))

    def __parse_semicolon_command(self, cmd_str, commands: list) -> int:
        """
        Functionality
        -------------
        To parse a command sequence; i.e. Rule: command ; command
        """
        start_slicing_index = 0
        while start_slicing_index < len(cmd_str):
            semi_colon_index = self.__find_first_non_quote_semicolon_index(
                cmd_str, start_slicing_index
            )
            commands.append(cmd_str[start_slicing_index:semi_colon_index])
            start_slicing_index = semi_colon_index + 1
        return 0

    def __replace_unquoted_double_ops_with_semicolon(
        self, cmdline: str
    ) -> int:
        quote = deque()

        i = 0
        while i < len(cmdline):
            if len(quote) != 0 and cmdline[i] == quote[0]:
                quote.popleft()
            elif cmdline[i] in {"'", '"', "`"}:
                quote.append(cmdline[i])

            if len(quote) == 0 and cmdline[i - 1] == "&" and cmdline[i] == "&":
                cmdline = cmdline[: i - 1] + ";" + cmdline[i + 1:]

            if len(quote) == 0 and cmdline[i - 1] == "|" and cmdline[i] == "|":
                cmdline = cmdline[: i - 1] + ";" + cmdline[i + 1:]
            i += 1

        return cmdline

    def __find_first_non_quote_semicolon_index(self, cmd_str, starting_index):
        """
        Functionality
        -------------
        Helper function for __parse_semicolon_command
        """
        quote = deque()
        for i in range(starting_index, len(cmd_str)):
            if len(quote) != 0 and cmd_str[i] == quote[0]:
                quote.popleft()
            elif cmd_str[i] in {"'", '"', "`"}:
                quote.append(cmd_str[i])

            if len(quote) == 0 and cmd_str[i] == ";":
                return i
        return len(cmd_str)

    def __hasPipe(self, s: str) -> str:
        """
        Functionality
        -------------
        Helper function for parse
        """
        pipe_in_str = "|" in s
        return pipe_in_str

    def getCommandSequence(self):
        return self._command_sequence

    def execute(self):
        """
        Functionality
        -------------
        To execute all commands in a sequence of commands
        and outputs the results of each command
        to the specified output of the shell
        """
        i = -1
        previous_stderr = True
        for command in self._command_sequence:
            command_output = command.execute()
            if i == -1:
                self._shell_stdOut.append(command_output.get_stdout() + " ")
            elif self._sequence_order[i] == ";" and not previous_stderr:
                exit()  # By specification of COMP0010 Shell
            elif self._sequence_order[i] == ";" and previous_stderr:
                self._shell_stdOut.append(command_output.get_stdout() + " ")
            elif self._sequence_order[i] == "||" and not previous_stderr:
                self._shell_stdOut.append(command_output.get_stdout() + " ")
            elif previous_stderr and self._sequence_order[i] == "&&":
                self._shell_stdOut.append(command_output.get_stdout() + " ")

            previous_stderr = command_output.get_stderr() and previous_stderr
            i += 1
        s = self._shell_stdOut[-1]
        self._shell_stdOut[-1] = s[: len(s) - 1]
        return 0
