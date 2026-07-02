# src/exceptions/authExceptions.py

class DuplicateEmailException(Exception):
    pass


class DuplicateUsernameException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class InvalidTokenException(Exception):
    pass