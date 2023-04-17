from command.Command import Command
from command.Call import Call


from collections import deque


PIPE = "|"


class Pipe(Command):
    def __init__(self, cmd_tokens=None, cmd_str=None):
        self.__calls = list()
        if cmd_tokens is None and cmd_str is None:
            return

        self.__parse(cmd_tokens, cmd_str)

    """PARSE"""

    def __parse(self, cmd_tokens, cmd_str):
        last_pipe_token_index = 0
        start_slicing_index = 0
        for token in range(len(cmd_tokens)):
            if cmd_tokens[token] == PIPE:
                pipe_index = self.__find_first_non_quote_pipe_index(
                    cmd_str, start_slicing_index
                )
                self.addCall(
                    Call(
                        cmd_tokens[last_pipe_token_index:token],
                        cmd_str[start_slicing_index:pipe_index],
                    )
                )
                start_slicing_index = pipe_index + 1
                last_pipe_token_index = token + 1
        self.addCall(
            Call(
                cmd_tokens[last_pipe_token_index:],
                cmd_str[start_slicing_index:],
            )
        )

    def __find_first_non_quote_pipe_index(self, cmd_str, starting_index):
        quote = deque()
        for i in range(starting_index, len(cmd_str)):
            if len(quote) != 0 and cmd_str[i] == quote[len(quote) - 1]:
                quote.pop()
            elif cmd_str[i] in {"'", '"', "`"}:
                quote.append(cmd_str[i])

            if len(quote) == 0 and cmd_str[i] == PIPE:
                return i
        return len(cmd_str) - 1

    """SETTER"""

    def addCall(self, call):
        self.__calls.append(call)

    """GETTER"""

    def getCalls(self):
        return self.__calls

    def requires_command_substitution(self):
        return any((c.requires_command_substitution() for c in self.__calls))

    def execute(self):
        app_sequence = deque()
        for call in self.__calls:
            app_sequence.append(call.try_create_application())

        app = app_sequence.popleft()
        app.set_app_sequence(app_sequence)

        app.run()
        return app

    # Override
    def print(self):
        for call in self.__calls:
            call.print()
