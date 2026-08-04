from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from app.commands.base import Command
from app.commands.registry import CommandRegistry, command_registry as default_command_registry
from app.plugins.event_bus import plugin_event_bus
from app.plugins.exceptions import PluginLoadError, PluginNotFound
from app.plugins.lifecycle import PluginRecord, PluginState
from app.plugins.loader import PluginLoader
from app.plugins.registry import plugin_registry


class PluginCommandAdapter(Command):
    def __init__(self, plugin_name: str, command: Any) -> None:
        self.name = getattr(command, "name", plugin_name)
        self.description = getattr(command, "description", "")
        self.args_schema = getattr(command, "args_schema", {})
        self.plugin_name = plugin_name
        self._command = command

    def validate(self, args: Dict[str, Any]) -> None:
        return self._command.validate(args)

    def execute(self, args: Dict[str, Any]) -> Any:
        return self._command.execute(args)

    def info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "args": self.args_schema,
        }


class PluginManager:
    def __init__(
        self,
        loader: Optional[PluginLoader] = None,
        registry: Optional[Any] = None,
        event_bus: Optional[Any] = None,
        command_registry: Optional[CommandRegistry] = None,
    ) -> None:
        self.loader = loader or PluginLoader()
        self.registry = registry or plugin_registry
        self.event_bus = event_bus or plugin_event_bus
        self.command_registry = command_registry or default_command_registry

    def discover(self) -> List[PluginRecord]:
        records: List[PluginRecord] = []
        for plugin_path in self.loader.discover_plugins():
            record = PluginRecord(name=plugin_path.parent.name, path=str(plugin_path), state=PluginState.DISCOVERED)
            self.registry.register(record)
            records.append(record)
            self.event_bus.emit("plugin.discovered", payload=record)
        return records

    def load(self, name: str) -> PluginRecord:
        record = self.registry.get(name)
        if record.instance is not None and record.state in {PluginState.INITIALIZED, PluginState.ENABLED}:
            return record

        plugin_path = Path(record.path)
        try:
            loaded = self.loader.load_plugin(plugin_path)
        except Exception as exc:
            record.state = PluginState.FAILED
            record.error = str(exc)
            self.event_bus.emit("plugin.failed", payload=record)
            raise PluginLoadError(str(exc)) from exc

        loaded.name = name
        loaded.state = PluginState.LOADED
        try:
            loaded.instance.initialize()
        except Exception as exc:
            loaded.state = PluginState.FAILED
            loaded.error = str(exc)
            self.registry.plugins[name] = loaded
            self.event_bus.emit("plugin.failed", payload=loaded)
            raise PluginLoadError(str(exc)) from exc

        loaded.state = PluginState.INITIALIZED
        self._register_commands(loaded)
        loaded.state = PluginState.ENABLED
        self.registry.plugins[name] = loaded
        self.event_bus.emit("plugin.loaded", payload=loaded, record=loaded)
        return loaded

    def unload(self, name: str) -> None:
        record = self.registry.get(name)
        if record.instance is not None:
            self._unregister_commands(record)
            record.instance.shutdown()
        record.state = PluginState.UNLOADED
        record.instance = None
        record.error = None
        self.event_bus.emit("plugin.unloaded", payload=record)

    def reload(self, name: str) -> PluginRecord:
        self.unload(name)
        return self.load(name)

    def list_plugins(self) -> List[PluginRecord]:
        return sorted(self.registry.list(), key=lambda item: item.name)

    def enable(self, name: str) -> PluginRecord:
        record = self.registry.get(name)
        if record.instance is None:
            return self.load(name)
        if record.state == PluginState.DISABLED:
            self._register_commands(record)
            record.state = PluginState.ENABLED
        else:
            record.state = PluginState.ENABLED
        self.event_bus.emit("plugin.enabled", payload=record)
        return record

    def disable(self, name: str) -> PluginRecord:
        record = self.registry.get(name)
        if record.instance is not None:
            self._unregister_commands(record)
        record.state = PluginState.DISABLED
        self.event_bus.emit("plugin.disabled", payload=record)
        return record

    def get(self, name: str) -> PluginRecord:
        return self.registry.get(name)

    def discover_and_load(self) -> List[PluginRecord]:
        self.discover()
        loaded: List[PluginRecord] = []
        for record in self.list_plugins():
            if record.state == PluginState.DISCOVERED:
                try:
                    loaded.append(self.load(record.name))
                except PluginLoadError:
                    continue
        return loaded

    def _register_commands(self, record: PluginRecord) -> None:
        if record.instance is None:
            return
        registered: List[str] = []
        for command in getattr(record.instance, "commands", []):
            adapter = PluginCommandAdapter(record.name, command)
            self.command_registry.register(adapter)
            registered.append(adapter.name)
        record.metadata["registered_commands"] = registered

    def _unregister_commands(self, record: PluginRecord) -> None:
        registered = record.metadata.get("registered_commands", [])
        for command_name in registered:
            self.command_registry.commands.pop(command_name, None)
        record.metadata["registered_commands"] = []


plugin_manager = PluginManager()
