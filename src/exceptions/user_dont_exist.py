class UserDontExists(Exception):
    def __init__(self, username) -> None:
        self._username = username
        super().__init__(
            f"You are trying to make an operation on an IncomingUser with username {self._username} that can not be "
            f"found "
        )
