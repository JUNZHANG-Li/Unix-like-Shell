class DirectoryNotFoundError(Exception):
    def __init__(
        self,
        app,
        directory,
        *args: object,
    ) -> None:
        super().__init__(args)
        self._app = app
        self._directory = directory

    def __str__(self) -> str:
        return (
            f"Directory Not Found Error -> application: {self._app} "
            f'cannot locate "{self._directory}"'
        )
