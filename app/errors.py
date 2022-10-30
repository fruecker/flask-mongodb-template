
class ErrorTracker:

    def __init__(self) -> None:
        self._last_error_msg = None
        self._last_error_type = None

    def get_last_error(self):
        return (self._last_error_msg, self._last_error_type)

    def _set_last_error(self, msg: str, _type:str = "danger"):
        self._last_error_msg = msg
        self._last_error_type = _type

class UserUndefinedError(Exception):
    pass

class InsufficentPermissonError(Exception):
    pass