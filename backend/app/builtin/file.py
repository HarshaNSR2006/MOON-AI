import os
import shutil
from pathlib import Path
from typing import Any, Dict

from app.commands.base import Command
from app.commands.exceptions import ExecutionFailed, InvalidArguments
from app.commands.result import CommandResult


class CreateFolderCommand(Command):
    name = "create_folder"
    description = "Create a folder at the specified path."
    args_schema = {"path": "The folder path to create."}

    def validate(self, args: Dict[str, Any]) -> None:
        path = args.get("path")
        if not isinstance(path, str) or not path.strip():
            raise InvalidArguments("A valid 'path' argument is required.")

    def execute(self, args: Dict[str, Any]) -> CommandResult:
        path = Path(args.get("path").strip())
        try:
            path.mkdir(parents=True, exist_ok=True)
            return CommandResult(
                success=True,
                command=self.name,
                message=f"Folder '{path}' created or already exists.",
                data={"path": str(path)},
            )
        except Exception as exc:
            raise ExecutionFailed(f"Unable to create folder '{path}': {exc}") from exc


class DeleteFileCommand(Command):
    name = "delete_file"
    description = "Delete a file at the specified path."
    args_schema = {"path": "The file path to delete."}

    def validate(self, args: Dict[str, Any]) -> None:
        path = args.get("path")
        if not isinstance(path, str) or not path.strip():
            raise InvalidArguments("A valid 'path' argument is required.")
        if not Path(path).exists():
            raise InvalidArguments(f"File or folder '{path}' does not exist.")

    def execute(self, args: Dict[str, Any]) -> CommandResult:
        path = Path(args.get("path").strip())
        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            return CommandResult(
                success=True,
                command=self.name,
                message=f"Deleted '{path}'.",
                data={"path": str(path)},
            )
        except Exception as exc:
            raise ExecutionFailed(f"Unable to delete '{path}': {exc}") from exc


class MoveFileCommand(Command):
    name = "move_file"
    description = "Move a file or folder from source to destination."
    args_schema = {"source": "Source path.", "destination": "Destination path."}

    def validate(self, args: Dict[str, Any]) -> None:
        source = args.get("source")
        destination = args.get("destination")
        if not isinstance(source, str) or not source.strip():
            raise InvalidArguments("A valid 'source' argument is required.")
        if not isinstance(destination, str) or not destination.strip():
            raise InvalidArguments("A valid 'destination' argument is required.")
        if not Path(source).exists():
            raise InvalidArguments(f"Source '{source}' does not exist.")

    def execute(self, args: Dict[str, Any]) -> CommandResult:
        source = Path(args.get("source").strip())
        destination = Path(args.get("destination").strip())
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            return CommandResult(
                success=True,
                command=self.name,
                message=f"Moved '{source}' to '{destination}'.",
                data={"source": str(source), "destination": str(destination)},
            )
        except Exception as exc:
            raise ExecutionFailed(f"Unable to move '{source}' to '{destination}': {exc}") from exc


class CopyFileCommand(Command):
    name = "copy_file"
    description = "Copy a file or folder from source to destination."
    args_schema = {"source": "Source path.", "destination": "Destination path."}

    def validate(self, args: Dict[str, Any]) -> None:
        source = args.get("source")
        destination = args.get("destination")
        if not isinstance(source, str) or not source.strip():
            raise InvalidArguments("A valid 'source' argument is required.")
        if not isinstance(destination, str) or not destination.strip():
            raise InvalidArguments("A valid 'destination' argument is required.")
        if not Path(source).exists():
            raise InvalidArguments(f"Source '{source}' does not exist.")

    def execute(self, args: Dict[str, Any]) -> CommandResult:
        source = Path(args.get("source").strip())
        destination = Path(args.get("destination").strip())
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(str(source), str(destination), dirs_exist_ok=True)
            else:
                shutil.copy2(str(source), str(destination))
            return CommandResult(
                success=True,
                command=self.name,
                message=f"Copied '{source}' to '{destination}'.",
                data={"source": str(source), "destination": str(destination)},
            )
        except Exception as exc:
            raise ExecutionFailed(f"Unable to copy '{source}' to '{destination}': {exc}") from exc


class ReadFileCommand(Command):
    name = "read_file"
    description = "Read the contents of a file."
    args_schema = {"path": "The file path to read."}

    def validate(self, args: Dict[str, Any]) -> None:
        path = args.get("path")
        if not isinstance(path, str) or not path.strip():
            raise InvalidArguments("A valid 'path' argument is required.")
        if not Path(path).is_file():
            raise InvalidArguments(f"File '{path}' does not exist or is not a file.")

    def execute(self, args: Dict[str, Any]) -> CommandResult:
        path = Path(args.get("path").strip())
        try:
            content = path.read_text(encoding="utf-8")
            return CommandResult(
                success=True,
                command=self.name,
                message=f"Read file '{path}'.",
                data={"path": str(path), "content": content},
            )
        except Exception as exc:
            raise ExecutionFailed(f"Unable to read file '{path}': {exc}") from exc


class WriteFileCommand(Command):
    name = "write_file"
    description = "Write content to a file, creating it if needed."
    args_schema = {"path": "The file path to write.", "content": "The text content to write."}

    def validate(self, args: Dict[str, Any]) -> None:
        path = args.get("path")
        content = args.get("content")
        if not isinstance(path, str) or not path.strip():
            raise InvalidArguments("A valid 'path' argument is required.")
        if not isinstance(content, str):
            raise InvalidArguments("A valid 'content' argument is required.")

    def execute(self, args: Dict[str, Any]) -> CommandResult:
        path = Path(args.get("path").strip())
        content = args.get("content")
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return CommandResult(
                success=True,
                command=self.name,
                message=f"Wrote file '{path}'.",
                data={"path": str(path)},
            )
        except Exception as exc:
            raise ExecutionFailed(f"Unable to write file '{path}': {exc}") from exc


class RenameFileCommand(Command):
    name = "rename_file"
    description = "Rename a file or folder."
    args_schema = {"source": "Source path.", "destination": "Destination path."}

    def validate(self, args: Dict[str, Any]) -> None:
        source = args.get("source")
        destination = args.get("destination")
        if not isinstance(source, str) or not source.strip():
            raise InvalidArguments("A valid 'source' argument is required.")
        if not isinstance(destination, str) or not destination.strip():
            raise InvalidArguments("A valid 'destination' argument is required.")
        if not Path(source).exists():
            raise InvalidArguments(f"Source '{source}' does not exist.")

    def execute(self, args: Dict[str, Any]) -> CommandResult:
        source = Path(args.get("source").strip())
        destination = Path(args.get("destination").strip())
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            source.rename(destination)
            return CommandResult(
                success=True,
                command=self.name,
                message=f"Renamed '{source}' to '{destination}'.",
                data={"source": str(source), "destination": str(destination)},
            )
        except Exception as exc:
            raise ExecutionFailed(f"Unable to rename '{source}' to '{destination}': {exc}") from exc
