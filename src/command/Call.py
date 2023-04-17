from command.Command import Command
from command.App_Factory import App_Factory
from Errors.UnsupportedApplicationError import UnsupportedApplicationError

import re


class string:
    def __init__(self) -> None:
        self.s = ""
        pass

    def get_str(self):
        return self.s

    def append(self, ss: str):
        self.s += ss


class Call(Command):
    def __init__(
        self,
        cmd_tokens: list = None,
        cmd_str: str = None,
    ):
        self.__app = None
        self.__args = list()

        if cmd_tokens is None and cmd_str is None:
            return None

        self.__parse(cmd_tokens, cmd_str)

    """PARSE"""

    def __parse(self, cmd_tokens, cmd_str):
        # isApplication = True
        cmd_str_index = 0
        token = 0
        while token < (len(cmd_tokens)):
            if cmd_tokens[token] == "Argument":
                current_argument = string()
                token += 1
                while token < len(cmd_tokens) and cmd_tokens[token] != " ":
                    cmd_str_index = self.__append_to_arg_given_token(
                        cmd_tokens,
                        token,
                        cmd_str,
                        cmd_str_index,
                        current_argument,
                    )
                    token += 1
                self.__append_to_args(current_argument.get_str())

            elif cmd_tokens[token] == "Redirection":
                current_argument = string()
                cmd_str_index = (
                    self.__append_to_args_and_increment_index(
                        cmd_str, cmd_str_index, current_argument
                    )
                    - 1
                )
                self.__append_to_args(current_argument.get_str())

            cmd_str_index += 1
            token += 1

    """PARSE HELPERS"""

    def __append_to_arg_given_token(
        self, cmd_tokens, token, cmd_str, cmd_str_index, argument: string
    ):
        if cmd_tokens[token] == "U":
            return self.__append_to_args_and_increment_index(
                cmd_str, cmd_str_index, argument
            )
        if cmd_tokens[token] in {"BQ", "SQ", "DQ"}:
            return self.__add_quoted_to_argument(
                cmd_str, cmd_str_index, argument, cmd_tokens, token
            )

    def __add_quoted_to_argument(
        self, cmd_str, cmd_str_index, argument: string, cmd_tokens, token
    ):
        quote = cmd_str[cmd_str_index]

        if (
            token != len(cmd_tokens) - 1
            and cmd_tokens[token] == "DQ"
            and cmd_tokens[token + 1] == "BQ"
        ):
            cmd_str_index = self.__append_to_args_and_increment_index(
                cmd_str, cmd_str_index, argument
            )
            while (
                cmd_str_index < len(cmd_str)
                and cmd_str[cmd_str_index] != quote
            ):
                if cmd_str[cmd_str_index] == "`":
                    cmd_str_index = self.__append_to_args_and_increment_index(
                        cmd_str, cmd_str_index, argument
                    )
                    while (
                        cmd_str_index < len(cmd_str)
                        and cmd_str[cmd_str_index] != "`"
                    ):
                        cmd_str_index = (
                            self.__append_to_args_and_increment_index(
                                cmd_str, cmd_str_index, argument
                            )
                        )
                    cmd_str_index = self.__append_to_args_and_increment_index(
                        cmd_str, cmd_str_index, argument
                    )
                cmd_str_index = self.__append_to_args_and_increment_index(
                    cmd_str, cmd_str_index, argument
                )

            if not cmd_str_index >= len(cmd_str):
                cmd_str_index = self.__append_to_args_and_increment_index(
                    cmd_str, cmd_str_index, argument
                )
            del cmd_tokens[token + 1]
        else:
            cmd_str_index = self.__append_to_args_and_increment_index(
                cmd_str, cmd_str_index, argument
            )
            while (
                cmd_str_index < len(cmd_str)
                and cmd_str[cmd_str_index] != quote
            ):
                cmd_str_index = self.__append_to_args_and_increment_index(
                    cmd_str, cmd_str_index, argument
                )
            cmd_str_index = self.__append_to_args_and_increment_index(
                cmd_str, cmd_str_index, argument
            )

        return cmd_str_index

    def __append_to_args_and_increment_index(
        self, str, index, argument: string
    ) -> int:
        argument.append(str[index])
        return index + 1

    def __append_to_args(self, arg: str) -> int:
        if len(self.__args) != 0:
            if self.__args[len(self.__args) - 1] in {"<", ">"}:
                self.__args[len(self.__args) - 1] += arg
                return 0

        self.__args.append(arg)

    """SETTER"""

    def set_app(self, arg):
        self.__app = arg

    def set_args(self, args):
        self.__args = args

    """GETTER"""

    def getApp(self):
        return self.__app

    def getArgs(self):
        return self.__args

    """COMMAND SUBSTITUTION HELPERS"""

    def requires_command_substitution(self):
        if self.__args is None:
            return False
        return any(
            (self.__contains_legal_backquoted(arg) for arg in self.__args)
        )

    """REQUIRES_COMMAND_SUBSTITUTION HELPERS"""

    def __contains_legal_backquoted(self, arg: str):
        if re.compile("[^`^']*(`.+`)[^`^']*").match(
            arg
        ) is not None and not self.__isSingleQuoted(arg):
            return True
        return False

    def __isSingleQuoted(self, arg):
        return arg[0] == "'" and arg[len(arg) - 1] == "'"

    """"""

    def execute(self):
        """
        Overiding superclass command's execute

        Functionality
        -------------
        To execute the the current call command
        (associated with an application and its arguments)

        Returns
        -------
        The stdout of the current call command
        (associated with an application and its arguments)
        """
        app = self.try_create_application()
        app.run()
        return app

    def try_create_application(self):
        """
        Functionality
        -------------
        Attempt to create an application from the App_Factory,
        otherwise print the exception message and crash

        Returns
        -------
        app : application
            an instance of application
        """
        try:
            app = App_Factory().create_application(self.__app, self.__args)
            return app
        except UnsupportedApplicationError as ua:
            print(ua)
            exit()

    def print(self):
        """
        Overiding superclass command's print

        Functionality
        -------------
        For Testing
        """

        print("Call:", self.__app, "->", self.__args)
