class IncorrectNumberOfRedirections(Exception):
    def __init__(
        self,
        app,
        *args: object,
    ) -> None:
        super().__init__(args)
        self._app = app

    def __str__(self) -> str:
        return f"Incorrect number of redirections -> {self._app}"
