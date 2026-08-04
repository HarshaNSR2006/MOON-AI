from typing import Dict, List

from app.commands.base import Command
from app.commands.exceptions import CommandNotFound


class CommandRegistry:
    def __init__(self) -> None:
        self.commands: Dict[str, Command] = {}

    def register(self, command: Command) -> None:
        self.commands[command.name] = command

    def get(self, name: str) -> Command:
        if name not in self.commands:
            raise CommandNotFound(f"Command '{name}' is not registered.")
        return self.commands[name]

    def list(self) -> List[Command]:
        return list(self.commands.values())


command_registry = CommandRegistry()

# Built-in commands are registered here to ensure they are available by default.
from app.builtin.browser import OpenURLCommand, SearchWebCommand
from app.builtin.desktop import OpenAppCommand
from app.builtin.file import (
    CreateFolderCommand,
    DeleteFileCommand,
    MoveFileCommand,
    CopyFileCommand,
    ReadFileCommand,
    WriteFileCommand,
    RenameFileCommand,
)
from app.builtin.system import CheckSystemCommand, ListProcessesCommand

command_registry.register(OpenAppCommand())
command_registry.register(OpenURLCommand())
command_registry.register(SearchWebCommand())
command_registry.register(CreateFolderCommand())
command_registry.register(DeleteFileCommand())
command_registry.register(MoveFileCommand())
command_registry.register(CopyFileCommand())
command_registry.register(ReadFileCommand())
command_registry.register(WriteFileCommand())
command_registry.register(RenameFileCommand())
command_registry.register(CheckSystemCommand())
command_registry.register(ListProcessesCommand())
