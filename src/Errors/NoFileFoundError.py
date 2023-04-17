class NoFileFoundError(Exception):
    def __init__(
        self,
        app,
        filename,
        *args: object,
    ) -> None:
        super().__init__(args)
        self._app = app
        self._filename = filename

    def __str__(self) -> str:
        return (
            f"No File Found Error -> application: {self._app} "
            f'cannot locate "{self._filename}"'
        )
