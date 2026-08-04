from typing import List


class ConversationSummarizer:
    def summarize(self, messages: List[str]) -> str:
        if not messages:
            return ""
        if len(messages) <= 5:
            return "\n".join(messages)
        return "... " + " ".join(messages[-5:])
