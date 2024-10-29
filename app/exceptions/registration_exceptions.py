class EmailAlreadyUsedError(Exception):

    def __init__(self, email: str) -> None:
        super().__init__()
        self.email = email


class BadImageProvidedError(Exception):

    def __init__(self) -> None:
        super().__init__()
        self.info = "Client provided bad or damaged image."
