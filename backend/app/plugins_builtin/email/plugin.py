from app.plugins.base import BasePlugin


class EmailPlugin(BasePlugin):
    name = "email"
    version = "1.0.0"
    author = "MOON AI"
    description = "Provides email-oriented commands"
    permissions = ["internet", "notifications"]

    def __init__(self) -> None:
        super().__init__()
        self.config = {"provider": "smtp"}

    def initialize(self) -> None:
        class EmailCommand:
            name = "send_email"
            description = "Send an email through the plugin"
            args_schema = {"to": "Recipient"}

            def validate(self, args):
                return None

            def execute(self, args):
                from app.commands.result import CommandResult

                return CommandResult(
                    success=True,
                    command=self.name,
                    message="Email plugin ready",
                    data={"to": args.get("to", "")},
                )

        self.register_command(EmailCommand())
        self.register_event("plugin_loaded")
