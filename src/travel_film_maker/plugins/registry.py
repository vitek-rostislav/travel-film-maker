from __future__ import annotations

from travel_film_maker.plugins.base import Plugin


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}

    def add(self, plugin: Plugin) -> None:
        self._plugins[plugin.name] = plugin
        plugin.register()

    def names(self) -> list[str]:
        return sorted(self._plugins)
