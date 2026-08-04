import os
import platform
import subprocess
from typing import Any, Dict, Optional

from app.commands.base import Command
from app.commands.exceptions import ExecutionFailed, InvalidArguments
from app.commands.result import CommandResult


class OpenAppCommand(Command):
    name = "open_app"
    description = "Open a desktop application by name or path."
    args_schema = {"name": "The application name or path."}

    def validate(self, args: Dict[str, Any]) -> None:
        name = args.get("name")
        if not isinstance(name, str) or not name.strip():
            raise InvalidArguments("A valid 'name' argument is required.")

    def execute(self, args: Dict[str, Any]) -> CommandResult:
        name = args.get("name").strip()
        try:
            if os.path.exists(name):
                if platform.system() == "Windows":
                    os.startfile(name)
                else:
                    subprocess.Popen([name])
            else:
                if platform.system() == "Windows":
                    subprocess.Popen(name, shell=True)
                elif platform.system() == "Darwin":
                    subprocess.Popen(["open", name])
                else:
                    subprocess.Popen([name])
            return CommandResult(
                success=True,
                command=self.name,
                message=f"Opening application '{name}'.",
                data={"name": name},
            )
        except Exception as exc:
            raise ExecutionFailed(f"Unable to open application '{name}': {exc}") from exc
