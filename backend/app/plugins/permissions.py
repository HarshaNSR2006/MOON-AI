from typing import Set

from app.plugins.exceptions import PluginPermissionError

DEFAULT_PERMISSIONS: Set[str] = {
    "filesystem",
    "internet",
    "desktop",
    "clipboard",
    "terminal",
}


def validate_permissions(permissions: set[str] | list[str] | None) -> list[str]:
    if permissions is None:
        return []
    if isinstance(permissions, set):
        normalized = list(permissions)
    else:
        normalized = list(permissions)
    for permission in normalized:
        if permission not in DEFAULT_PERMISSIONS and permission not in {"notifications", "microphone", "camera"}:
            raise PluginPermissionError(f"Unsupported permission '{permission}'.")
    return normalized
