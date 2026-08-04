class CommandError(Exception):
    pass


class CommandNotFound(CommandError):
    pass


class InvalidArguments(CommandError):
    pass


class PermissionDenied(CommandError):
    pass


class ExecutionFailed(CommandError):
    pass


class CommandTimeout(ExecutionFailed):
    pass
