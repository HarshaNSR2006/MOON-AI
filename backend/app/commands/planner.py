import re
from typing import List, Optional

from app.schemas.command import CommandPlan, CommandPlanRequest, CommandStep


class CommandPlanner:
    def __init__(self) -> None:
        self.patterns = [
            (r"\bopen\b.*\b(vs code|code)\b", self._open_editor),
            (r"\bopen\b.*\b(chrome|browser|edge|firefox|safari)\b", self._open_browser),
            (r"\bsearch\b.*\b(web|google|internet|documentation|docs)\b", self._search_web),
            (r"\bsearch\b.*", self._search_web),
            (r"\bopen\b.*\burl\b", self._open_url),
            (r"\bgo to\b.*", self._open_url),
            (r"\bcreate\b.*\bfolder\b", self._create_folder),
            (r"\bmake\b.*\bfolder\b", self._create_folder),
            (r"\bread\b.*\bfile\b", self._read_file),
            (r"\bwrite\b.*\bfile\b", self._write_file),
            (r"\bdelete\b.*\bfile\b", self._delete_file),
            (r"\brename\b.*\bfile\b", self._rename_file),
            (r"\bcopy\b.*\bfile\b", self._copy_file),
            (r"\bmove\b.*\bfile\b", self._move_file),
            (r"\blist\b.*\bprocess(es)?\b", self._list_processes),
            (r"\b(system|status)\b", self._check_system),
        ]

    def plan(self, request: CommandPlanRequest) -> CommandPlan:
        query = request.query.strip()
        if not query:
            return CommandPlan(steps=[])

        fragments = re.split(r"\band then\b|\bthen\b", query, flags=re.IGNORECASE)
        steps: List[CommandStep] = []

        for fragment in fragments:
            fragment = fragment.strip()
            if not fragment:
                continue
            step = self._plan_fragment(fragment, request.conversation_id)
            if step is not None:
                steps.append(step)

        return CommandPlan(steps=steps)

    def _plan_fragment(self, fragment: str, conversation_id: Optional[str]) -> Optional[CommandStep]:
        for pattern, handler in self.patterns:
            if re.search(pattern, fragment, flags=re.IGNORECASE):
                return handler(fragment, conversation_id)
        return self._infer_generic_step(fragment, conversation_id)

    def _infer_generic_step(
        self,
        fragment: str,
        conversation_id: Optional[str],
    ) -> Optional[CommandStep]:
        if fragment.lower().startswith("open "):
            target = fragment[5:].strip()
            return CommandStep(command="open_app", args={"name": target})
        if fragment.lower().startswith("delete ") and "file" in fragment.lower():
            path = self._extract_path(fragment, r"delete file (.+)")
            return CommandStep(command="delete_file", args={"path": path})
        if fragment.lower().startswith("read ") and "file" in fragment.lower():
            path = self._extract_path(fragment, r"read file (.+)")
            return CommandStep(command="read_file", args={"path": path})
        return CommandStep(command="search_web", args={"query": fragment})

    def _extract_path(self, fragment: str, pattern: str) -> str:
        match = re.search(pattern, fragment, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip(" '\"")
        return fragment

    def _open_editor(self, fragment: str, conversation_id: Optional[str]) -> CommandStep:
        return CommandStep(command="open_app", args={"name": "code"})

    def _open_browser(self, fragment: str, conversation_id: Optional[str]) -> CommandStep:
        browser = self._extract_path(fragment, r"open (.+)")
        return CommandStep(command="open_app", args={"name": browser})

    def _search_web(self, fragment: str, conversation_id: Optional[str]) -> CommandStep:
        query = self._extract_path(fragment, r"search (?:the )?(?:web )?(?:for )?(.+)")
        return CommandStep(command="search_web", args={"query": query})

    def _open_url(self, fragment: str, conversation_id: Optional[str]) -> CommandStep:
        url = self._extract_path(fragment, r"(?:open|go to) (.+)")
        return CommandStep(command="open_url", args={"url": url})

    def _create_folder(self, fragment: str, conversation_id: Optional[str]) -> CommandStep:
        folder = self._extract_path(fragment, r"(?:create|make) folder (.+)")
        return CommandStep(command="create_folder", args={"path": folder})

    def _read_file(self, fragment: str, conversation_id: Optional[str]) -> CommandStep:
        path = self._extract_path(fragment, r"read file (.+)")
        return CommandStep(command="read_file", args={"path": path})

    def _write_file(self, fragment: str, conversation_id: Optional[str]) -> CommandStep:
        match = re.search(r"write file (.+?) (?:with|containing|content) (.+)", fragment, flags=re.IGNORECASE)
        if match:
            return CommandStep(
                command="write_file",
                args={"path": match.group(1).strip(" '\""), "content": match.group(2).strip(" '\"")},
            )
        return CommandStep(command="write_file", args={"path": fragment, "content": ""})

    def _delete_file(self, fragment: str, conversation_id: Optional[str]) -> CommandStep:
        path = self._extract_path(fragment, r"delete file (.+)")
        return CommandStep(command="delete_file", args={"path": path})

    def _rename_file(self, fragment: str, conversation_id: Optional[str]) -> CommandStep:
        match = re.search(r"rename file (.+?) to (.+)", fragment, flags=re.IGNORECASE)
        if match:
            return CommandStep(
                command="rename_file",
                args={"source": match.group(1).strip(" '\""), "destination": match.group(2).strip(" '\"")},
            )
        return CommandStep(command="rename_file", args={"source": fragment, "destination": ""})

    def _copy_file(self, fragment: str, conversation_id: Optional[str]) -> CommandStep:
        match = re.search(r"copy file (.+?) to (.+)", fragment, flags=re.IGNORECASE)
        if match:
            return CommandStep(
                command="copy_file",
                args={"source": match.group(1).strip(" '\""), "destination": match.group(2).strip(" '\"")},
            )
        return CommandStep(command="copy_file", args={"source": fragment, "destination": ""})

    def _move_file(self, fragment: str, conversation_id: Optional[str]) -> CommandStep:
        match = re.search(r"move file (.+?) to (.+)", fragment, flags=re.IGNORECASE)
        if match:
            return CommandStep(
                command="move_file",
                args={"source": match.group(1).strip(" '\""), "destination": match.group(2).strip(" '\"")},
            )
        return CommandStep(command="move_file", args={"source": fragment, "destination": ""})

    def _list_processes(self, fragment: str, conversation_id: Optional[str]) -> CommandStep:
        return CommandStep(command="list_processes", args={})

    def _check_system(self, fragment: str, conversation_id: Optional[str]) -> CommandStep:
        return CommandStep(command="check_system", args={})
