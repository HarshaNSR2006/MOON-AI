from __future__ import annotations

from typing import Dict, List

from app.plugins.exceptions import PluginNotFound
from app.plugins.lifecycle import PluginRecord


class PluginRegistry:
    def __init__(self) -> None:
        self.plugins: Dict[str, PluginRecord] = {}

    def register(self, record: PluginRecord) -> None:
        self.plugins[record.name] = record

    def get(self, name: str) -> PluginRecord:
        if name not in self.plugins:
            raise PluginNotFound(f"Plugin '{name}' is not registered.")
        return self.plugins[name]

    def list(self) -> List[PluginRecord]:
        return list(self.plugins.values())


plugin_registry = PluginRegistry()
