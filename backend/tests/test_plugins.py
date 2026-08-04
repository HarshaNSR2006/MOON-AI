from pathlib import Path
from textwrap import dedent

from app.commands.registry import CommandRegistry
from app.plugins.event_bus import PluginEventBus
from app.plugins.lifecycle import PluginState
from app.plugins.loader import PluginLoader
from app.plugins.manager import PluginManager
from app.plugins.registry import PluginRegistry


def test_plugin_manager_discovers_builtin_plugins() -> None:
    plugin_root = Path(__file__).resolve().parents[1] / "app" / "plugins_builtin"
    registry = PluginRegistry()
    manager = PluginManager(loader=PluginLoader(plugin_root=plugin_root), registry=registry)

    discovered = manager.discover()

    assert {record.name for record in discovered} >= {"browser", "filesystem", "github", "email"}


def test_plugin_manager_loads_plugin_and_registers_commands() -> None:
    plugin_root = Path(__file__).resolve().parents[1] / "app" / "plugins_builtin"
    registry = PluginRegistry()
    command_registry = CommandRegistry()
    manager = PluginManager(
        loader=PluginLoader(plugin_root=plugin_root),
        registry=registry,
        command_registry=command_registry,
    )

    manager.discover()
    loaded = manager.load("browser")

    assert loaded.state == PluginState.ENABLED
    assert command_registry.get("open_browser_plugin").name == "open_browser_plugin"

    manager.disable("browser")
    assert "open_browser_plugin" not in command_registry.commands

    manager.enable("browser")
    assert command_registry.get("open_browser_plugin").name == "open_browser_plugin"


def test_plugin_loader_applies_config_and_event_bus_notifies() -> None:
    plugin_root = Path(__file__).resolve().parents[1] / "app" / "plugins_builtin"
    loader = PluginLoader(plugin_root=plugin_root)
    bus = PluginEventBus()
    events: list[tuple[str, object]] = []

    def capture(event_name: str, payload: object | None = None, **_: object) -> None:
        events.append((event_name, payload))

    bus.subscribe("plugin.loaded", capture)
    record = loader.load_plugin(plugin_root / "browser" / "plugin.py")
    assert record.instance is not None
    assert record.instance.config.get("default_browser") == "chrome"

    bus.emit("plugin.loaded", payload=record)
    assert events[-1][0] == "plugin.loaded"
    assert events[-1][1] is record


def test_plugin_loader_reads_python_config_from_config_file(tmp_path: Path) -> None:
    plugin_dir = tmp_path / "demo"
    plugin_dir.mkdir()
    (plugin_dir / "config.py").write_text(
        dedent(
            """
            CONFIG = {"enabled": True, "default_mode": "safe"}
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    (plugin_dir / "plugin.py").write_text(
        dedent(
            """
            from app.plugins.base import BasePlugin

            class DemoPlugin(BasePlugin):
                name = "demo"

                def __init__(self) -> None:
                    super().__init__()
                    self.config = {}

                def initialize(self) -> None:
                    pass
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )

    loader = PluginLoader(plugin_root=tmp_path)
    record = loader.load_plugin(plugin_dir / "plugin.py")

    assert record.instance is not None
    assert record.instance.config.get("enabled") is True
    assert record.instance.config.get("default_mode") == "safe"
