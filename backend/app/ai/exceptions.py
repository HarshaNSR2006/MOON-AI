class AIError(Exception):
    """Base exception for AI manager errors."""


class AIProviderUnavailable(AIError):
    pass


class InvalidModel(AIError):
    pass


class ContextTooLarge(AIError):
    pass


class StreamingError(AIError):
    pass


class AuthenticationError(AIError):
    pass
