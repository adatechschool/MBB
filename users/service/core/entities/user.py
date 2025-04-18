# users\service\core\entities\user.py

"""Module containing the User entity class for the authentication service."""


class UserEntity:
    """Entity class representing a user in the authentication service.

    Contains core user attributes including id, username, email and hashed password.
    """

    def __init__(self, user_id: int, username: str, email: str, hashed_password: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

    def __repr__(self):
        return f"<UserEntity id={self.user_id} username={self.username}>"
