from app.plugins.base import BasePlugin


class BrowserPlugin(BasePlugin):
    name = "browser"
    version = "1.0.0"
    author = "MOON AI"
    description = "Provides browser-oriented commands"
    permissions = ["internet", "desktop"]

    def __init__(self) -> None:
        super().__init__()
        self.config = {"default_browser": "chrome"}

    def initialize(self) -> None:
        class BrowserCommand:
            name = "open_browser_plugin"
            description = "Open a browser through the plugin"
            args_schema = {"url": "URL to open"}

            def validate(self, args):
                return None

            def execute(self, args):
                from app.commands.result import CommandResult

                return CommandResult(
                    success=True,
                    command=self.name,
                    message="Browser plugin loaded",
                    data={"url": args.get("url", "")},
                )

        self.register_command(BrowserCommand())
        self.register_event("plugin_loaded")
