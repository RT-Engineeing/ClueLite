class GameException(Exception):
    pass


class InvalidPlayerException(GameException):
    def __init__(self):
        message = "The specified player does not exist."
        super(InvalidPlayerException, self).__init__(message)


class InvalidRoomException(GameException):
    def __init__(self):
        message = "The specified room does not exist."
        super(InvalidRoomException, self).__init__(message)


class InvalidPlayerTurnException(GameException):
    def __init__(self):
        message = "The attempted operation is invalid. Player is out of turn."
        super(InvalidPlayerTurnException, self).__init__(message)


class InvalidPlayerSuspectException(GameException):
    def __init__(self):
        message = "The attempted operation is invalid. Invalid suspect."
        super(InvalidPlayerSuspectException, self).__init__(message)


class InvalidPlayerIsSuspectException(GameException):
    def __init__(self):
        message = "The attempted operation is invalid. Suspect does not belong to player."
        super(InvalidPlayerIsSuspectException, self).__init__(message)


class InvalidSuggestionRoomException(GameException):
    def __init__(self):
        message = "The attempted operation is invalid. Player must be in the room associated to the suggestion."
        super(InvalidSuggestionRoomException, self).__init__(message)

class InvalidEmptyRoomException(GameException):
    def __init__(self):
        message = "The attempted operation is invalid. This room is unavailable."
        super(InvalidEmptyRoomException, self).__init__(message)