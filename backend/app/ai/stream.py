from typing import AsyncGenerator


def format_sse_event(data: str) -> str:
    return f"data: {data}\n\n"


async def stream_text_chunks(chunks: AsyncGenerator[str, None]):
    async for chunk in chunks:
        yield format_sse_event(chunk)
