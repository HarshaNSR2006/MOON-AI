from app.plugins.base import BasePlugin


class GitHubPlugin(BasePlugin):
    name = "github"
    version = "1.0.0"
    author = "MOON AI"
    description = "Provides GitHub commands"
    permissions = ["internet", "filesystem"]

    def __init__(self) -> None:
        super().__init__()
        self.config = {"api_url": "https://api.github.com"}

    def initialize(self) -> None:
        class GitHubCommand:
            name = "list_github_repos"
            description = "List repositories from GitHub"
            args_schema = {"owner": "GitHub owner"}

            def validate(self, args):
                return None

            def execute(self, args):
                from app.commands.result import CommandResult

                return CommandResult(
                    success=True,
                    command=self.name,
                    message="GitHub plugin ready",
                    data={"owner": args.get("owner", "")},
                )

        self.register_command(GitHubCommand())
        self.register_event("plugin_loaded")
