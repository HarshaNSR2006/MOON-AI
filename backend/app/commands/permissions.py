from app.commands.exceptions import PermissionDenied


RESTRICTED_COMMANDS = {
    "delete_file",
    "delete_folder",
    "shutdown_pc",
    "restart_pc",
    "run_shell_command",
}


def check_permission(command_name: str, allow_dangerous: bool = False) -> None:
    if command_name in RESTRICTED_COMMANDS and not allow_dangerous:
        raise PermissionDenied(
            f"Command '{command_name}' is restricted. Set allow_dangerous=true to execute."
        )
