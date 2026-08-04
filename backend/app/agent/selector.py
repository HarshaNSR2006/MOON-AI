from __future__ import annotations

from typing import Dict, List

from app.commands.registry import command_registry
from app.plugins.manager import plugin_manager


class ToolSelector:
    def __init__(self) -> None:
        self.plugin_manager = plugin_manager
        self.command_registry = command_registry

    def select_tools(self, goal: str) -> Dict[str, List[str]]:
        tools: List[str] = []
        commands = [command.name for command in self.command_registry.list()]
        plugins = [plugin.name for plugin in self.plugin_manager.list_plugins()]

        lower = goal.lower()
        if any(keyword in lower for keyword in ["browser", "search", "open url", "google"]):
            if "browser" in plugins:
                tools.append("browser")
            if "search_web" in commands:
                tools.append("search_web")
        if any(keyword in lower for keyword in ["file", "folder", "create", "delete", "move", "copy"]):
            if "filesystem" in plugins:
                tools.append("filesystem")
            if "read_file" in commands:
                tools.append("filesystem")
        if any(keyword in lower for keyword in ["open", "launch", "run"]):
            tools.append("desktop")
        if not tools:
            tools.append("general")

        return {"commands": commands, "plugins": plugins, "selected": tools}
