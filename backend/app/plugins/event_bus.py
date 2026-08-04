from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional


class PluginEventBus:
    def __init__(self) -> None:
        self._listeners: Dict[str, List[Callable[..., None]]] = {}

    def subscribe(self, event_name: str, handler: Callable[..., None]) -> None:
        self._listeners.setdefault(event_name, []).append(handler)

    def emit(self, event_name: str, payload: Optional[object] = None, **kwargs: Any) -> None:
        for handler in self._listeners.get(event_name, []):
            try:
                handler(event_name, payload, **kwargs)
            except TypeError:
                try:
                    handler(payload, **kwargs)
                except TypeError:
                    handler()


plugin_event_bus = PluginEventBus()
