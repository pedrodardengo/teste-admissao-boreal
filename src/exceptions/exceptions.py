class InvalidUsernameOrPassword(Exception):
    def __init__(self) -> None:
        super().__init__()


class UserAlreadyExists(Exception):
    def __init__(self, username) -> None:
        self.username = username
        super().__init__()


class UserDontExists(Exception):
    def __init__(self) -> None:
        super().__init__()


class TokenHasExpired(Exception):
    def __init__(self) -> None:
        super().__init__()


class CouldNotValidate(Exception):
    def __init__(self) -> None:
        super().__init__()
