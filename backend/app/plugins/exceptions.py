class PluginError(Exception):
    pass


class PluginNotFound(PluginError):
    pass


class PluginAlreadyLoaded(PluginError):
    pass


class PluginLoadError(PluginError):
    pass


class PluginValidationError(PluginError):
    pass


class PluginPermissionError(PluginError):
    pass
