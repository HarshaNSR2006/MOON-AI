from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.plugins.exceptions import PluginLoadError, PluginNotFound
from app.plugins.lifecycle import PluginRecord
from app.plugins.manager import plugin_manager
from app.schemas.plugin import PluginInfo

router = APIRouter()


def _to_plugin_info(record: PluginRecord) -> PluginInfo:
    return PluginInfo(
        name=record.name,
        path=record.path,
        state=record.state.value,
        manifest=record.manifest,
        error=record.error,
        metadata=record.metadata,
    )


@router.get("", response_model=list[PluginInfo])
def list_plugins(current_user=Depends(get_current_user)) -> list[PluginInfo]:
    return [_to_plugin_info(record) for record in plugin_manager.list_plugins()]


@router.post("/discover", response_model=list[PluginInfo])
def discover_plugins(current_user=Depends(get_current_user)) -> list[PluginInfo]:
    discovered = plugin_manager.discover_and_load()
    return [_to_plugin_info(record) for record in discovered]


@router.get("/{name}", response_model=PluginInfo)
def get_plugin(name: str, current_user=Depends(get_current_user)) -> PluginInfo:
    try:
        return _to_plugin_info(plugin_manager.get(name))
    except PluginNotFound as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/load", response_model=PluginInfo)
def load_plugin(name: str, current_user=Depends(get_current_user)) -> PluginInfo:
    try:
        return _to_plugin_info(plugin_manager.load(name))
    except PluginLoadError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/unload", response_model=PluginInfo)
def unload_plugin(name: str, current_user=Depends(get_current_user)) -> PluginInfo:
    try:
        plugin_manager.unload(name)
        return _to_plugin_info(plugin_manager.get(name))
    except PluginNotFound as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/reload", response_model=PluginInfo)
def reload_plugin(name: str, current_user=Depends(get_current_user)) -> PluginInfo:
    try:
        return _to_plugin_info(plugin_manager.reload(name))
    except PluginLoadError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.patch("/{name}/enable", response_model=PluginInfo)
def enable_plugin(name: str, current_user=Depends(get_current_user)) -> PluginInfo:
    return _to_plugin_info(plugin_manager.enable(name))


@router.patch("/{name}/disable", response_model=PluginInfo)
def disable_plugin(name: str, current_user=Depends(get_current_user)) -> PluginInfo:
    return _to_plugin_info(plugin_manager.disable(name))
