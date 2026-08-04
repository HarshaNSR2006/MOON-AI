from __future__ import annotations

from typing import Any, Dict


class PluginSandbox:
    def __init__(self, plugin_name: str) -> None:
        self.plugin_name = plugin_name

    def validate(self, plugin: Any) -> None:
        if not hasattr(plugin, "initialize"):
            raise RuntimeError(f"Plugin '{self.plugin_name}' is missing initialize().")
