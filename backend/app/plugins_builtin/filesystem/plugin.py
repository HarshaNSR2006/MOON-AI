from app.plugins.base import BasePlugin


class FilesystemPlugin(BasePlugin):
    name = "filesystem"
    version = "1.0.0"
    author = "MOON AI"
    description = "Provides filesystem-oriented commands"
    permissions = ["filesystem"]

    def __init__(self) -> None:
        super().__init__()
        self.config = {"root": "."}

    def initialize(self) -> None:
        class FilesystemCommand:
            name = "list_plugin_files"
            description = "List files via the plugin"
            args_schema = {"path": "Directory to inspect"}

            def validate(self, args):
                return None

            def execute(self, args):
                from app.commands.result import CommandResult
                from pathlib import Path

                path = Path(args.get("path", "."))
                return CommandResult(
                    success=True,
                    command=self.name,
                    message="Listed files via plugin",
                    data={"path": str(path), "files": [p.name for p in path.iterdir()]},
                )

        self.register_command(FilesystemCommand())
        self.register_event("plugin_loaded")
