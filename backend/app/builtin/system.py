import os
import platform
import subprocess
from typing import Any, Dict, List

from app.commands.base import Command
from app.commands.exceptions import ExecutionFailed
from app.commands.result import CommandResult


class CheckSystemCommand(Command):
    name = "check_system"
    description = "Return basic system information."
    args_schema = {}

    def validate(self, args: Dict[str, Any]) -> None:
        if args:
            raise ExecutionFailed("check_system does not accept arguments.")

    def execute(self, args: Dict[str, Any]) -> CommandResult:
        try:
            info = {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "architecture": platform.machine(),
                "cpu_count": os.cpu_count(),
            }
            if hasattr(os, "getloadavg"):
                info["load_average"] = os.getloadavg()
            return CommandResult(
                success=True,
                command=self.name,
                message="Collected basic system information.",
                data=info,
            )
        except Exception as exc:
            raise ExecutionFailed(f"Unable to collect system information: {exc}") from exc


class ListProcessesCommand(Command):
    name = "list_processes"
    description = "List running processes on the machine."
    args_schema = {}

    def validate(self, args: Dict[str, Any]) -> None:
        if args:
            raise ExecutionFailed("list_processes does not accept arguments.")

    def execute(self, args: Dict[str, Any]) -> CommandResult:
        try:
            process_names: List[str] = []
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["tasklist"], capture_output=True, text=True, check=True
                )
                lines = result.stdout.splitlines()[3:]
                process_names = [line.split()[0] for line in lines if line.strip()]
            else:
                result = subprocess.run(
                    ["ps", "-e", "-o", "comm="], capture_output=True, text=True, check=True
                )
                process_names = [line.strip() for line in result.stdout.splitlines() if line.strip()]

            return CommandResult(
                success=True,
                command=self.name,
                message=f"Found {len(process_names)} running processes.",
                data={"processes": process_names},
            )
        except Exception as exc:
            raise ExecutionFailed(f"Unable to list processes: {exc}") from exc
