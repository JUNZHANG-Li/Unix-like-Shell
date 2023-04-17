class UnsupportedApplicationError(Exception):
    def __init__(self, application_name: str, *args: object) -> None:
        super().__init__(args)
        self.application_name = application_name

    def __str__(self) -> str:
        return (
            f"Unsupported Application -> application: "
            f'"{self.application_name}" is not supported'
        )
