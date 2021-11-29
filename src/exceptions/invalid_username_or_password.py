class InvalidUsernameOrPassword(Exception):
    def __init__(self) -> None:
        super().__init__("Username or password is invalid")
