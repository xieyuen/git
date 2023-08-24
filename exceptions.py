# Exceptions

class UndefinedError(Exception):
    ...


class DisableError(Exception):
    ...


# Unknown Exceptions
class UnknownArgumentError(Exception):
    ...


class UnknownFunctionError(Exception):
    ...


class UnknownMethodError(Exception):
    ...


class UnknownCommandError(Exception):
    ...


class UnknownCommandNodeError(Exception):
    ...


class InvalidArgumentError(Exception):
    ...


class CommandParseError(Exception):
    ...


class Finish(Exception):
    ...


class FileError(Exception):
    ...


class IndefiniteError(Exception):
    ...
