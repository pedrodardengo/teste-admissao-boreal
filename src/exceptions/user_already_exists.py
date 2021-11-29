class UserAlreadyExists(Exception):
    def __init__(self, username) -> None:
        self._username = username
        super().__init__(f"The username: {self._username} is already in use")
