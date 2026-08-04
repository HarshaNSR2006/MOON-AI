import webbrowser
from typing import Any, Dict
from urllib.parse import quote

from app.commands.base import Command
from app.commands.result import CommandResult
from app.commands.exceptions import InvalidArguments


class OpenURLCommand(Command):
    name = "open_url"
    description = "Open a URL in the system browser."
    args_schema = {"url": "The URL to open."}

    def validate(self, args: Dict[str, Any]) -> None:
        url = args.get("url")
        if not isinstance(url, str) or not url.strip():
            raise InvalidArguments("A valid 'url' argument is required.")

    def execute(self, args: Dict[str, Any]) -> CommandResult:
        url = args.get("url").strip()
        opened = webbrowser.open(url)
        return CommandResult(
            success=bool(opened),
            command=self.name,
            message=f"Opened URL '{url}'." if opened else f"Unable to open URL '{url}'.",
            data={"url": url},
            error=None if opened else "OPEN_FAILED",
        )


class SearchWebCommand(Command):
    name = "search_web"
    description = "Search the web for a query using the default browser."
    args_schema = {"query": "Search query text."}

    def validate(self, args: Dict[str, Any]) -> None:
        query = args.get("query")
        if not isinstance(query, str) or not query.strip():
            raise InvalidArguments("A valid 'query' argument is required.")

    def execute(self, args: Dict[str, Any]) -> CommandResult:
        query = args.get("query").strip()
        url = f"https://www.google.com/search?q={quote(query)}"
        opened = webbrowser.open(url)
        return CommandResult(
            success=bool(opened),
            command=self.name,
            message=f"Opened browser search for '{query}'." if opened else f"Unable to open browser search for '{query}'.",
            data={"query": query, "search_url": url},
            error=None if opened else "SEARCH_FAILED",
        )
