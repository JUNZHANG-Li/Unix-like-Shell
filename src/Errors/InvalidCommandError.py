class InvalidCommandError(Exception):
    def __init__(self, cmdline: str, *args: object) -> None:
        super().__init__(args)
        self.cmdline = cmdline

    def __str__(self) -> str:
        return f"syntax error: {self.cmdline} is not a valid command"
