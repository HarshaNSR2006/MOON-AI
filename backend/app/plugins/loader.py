from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from app.plugins.base import BasePlugin
from app.plugins.exceptions import PluginLoadError, PluginValidationError
from app.plugins.lifecycle import PluginRecord, PluginState
from app.plugins.permissions import validate_permissions


class PluginLoader:
    def __init__(self, plugin_root: Optional[Path] = None) -> None:
        self.plugin_root = plugin_root or Path(__file__).resolve().parent.parent / "plugins_builtin"

    def discover_plugins(self) -> list[Path]:
        if not self.plugin_root.exists():
            return []
        return sorted([path for path in self.plugin_root.glob("**/plugin.py") if path.is_file()])

    def _load_plugin_config(self, plugin_dir: Path) -> Dict[str, Any]:
        for candidate in (plugin_dir / "config.json", plugin_dir / "config.py"):
            if not candidate.exists():
                continue
            if candidate.suffix == ".json":
                with candidate.open("r", encoding="utf-8") as handle:
                    return json.load(handle)
            if candidate.suffix == ".py":
                module_name = f"moon_plugin_config_{abs(hash(candidate))}"
                spec = importlib.util.spec_from_file_location(module_name, candidate)
                if spec is None or spec.loader is None:
                    return {}
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                try:
                    spec.loader.exec_module(module)
                except Exception:
                    return {}

                for attr_name in ("CONFIG", "config"):
                    value = getattr(module, attr_name, None)
                    if isinstance(value, dict):
                        return dict(value)

                for attr_name in dir(module):
                    if attr_name.startswith("_"):
                        continue
                    value = getattr(module, attr_name)
                    if isinstance(value, dict):
                        return dict(value)
                return {}
        return {}

    def load_plugin(self, path: Path) -> PluginRecord:
        if not path.exists():
            raise PluginLoadError(f"Plugin file '{path}' does not exist.")

        module_name = f"moon_plugin_{path.stem}_{abs(hash(path))}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise PluginLoadError(f"Unable to load plugin module from '{path}'.")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        plugin_class = None
        for attr_name in dir(module):
            value = getattr(module, attr_name)
            if isinstance(value, type) and issubclass(value, BasePlugin) and value is not BasePlugin:
                plugin_class = value
                break

        if plugin_class is None:
            raise PluginLoadError(f"Plugin module '{path}' does not define a valid BasePlugin subclass.")

        plugin = plugin_class()
        plugin.config.update(self._load_plugin_config(path.parent))
        manifest = plugin.get_manifest()
        try:
            validate_permissions(plugin.permissions)
        except Exception as exc:
            raise PluginValidationError(str(exc)) from exc

        return PluginRecord(
            name=plugin.name or path.parent.name,
            path=str(path),
            state=PluginState.LOADED,
            manifest=manifest,
            instance=plugin,
        )
