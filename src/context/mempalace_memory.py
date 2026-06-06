"""MemPalace stub — redirects to RAG indexer (ChromaDB not installed).

All calls transparently use the working RAG/Ollama pipeline instead.
"""

from __future__ import annotations

import structlog

logger = structlog.get_logger()


async def store_interaction(user_message: str, assistant_response: str) -> None:
    """Store conversation in RAG vector store."""
    try:
        from src.rag.indexer import RAGIndexer

        rag = RAGIndexer()
        text = f"[Usuario]: {user_message[:400]}\n[AURA]: {assistant_response[:600]}"
        await rag.index_text(text, "telegram_chat", "memory")
    except Exception as exc:
        logger.debug("mempalace_rag_error", error=str(exc))


async def search_memory(query: str, top_k: int = 5) -> list:
    """Search conversation memory via RAG."""
    try:
        from src.rag.retriever import RAGRetriever

        retriever = RAGRetriever()
        return await retriever.search(query, top_k=top_k, source_types=["memory"])
    except Exception:
        return []


# Alias for compatibility
async def search_memories(query: str, n: int = 5) -> list:
    """Alias for search_memory (plural form for backwards compat)."""
    return await search_memory(query, top_k=n)


def format_memories_for_prompt(memories: list) -> str:
    """Format RAG results as text for LLM prompt."""
    if not memories:
        return "No relevant memories found."
    lines = []
    for i, mem in enumerate(memories, 1):
        text = mem.get("content", "")[
            :300
        ]  # RAGRetriever returns "content", not "text"
        score = mem.get("score", 0.0)
        lines.append(f"{i}. [{score:.2f}] {text}")
    return "\n".join(lines)


async def palace_count() -> int:
    """Return count of stored memories."""
    try:
        from src.rag.retriever import RAGRetriever

        retriever = RAGRetriever()
        status = await retriever.status()
        return status.get("total_chunks", 0)
    except Exception:
        return 0


async def get_all_memories(limit: int = 10) -> list:
    """Get most recent memories (stub — returns empty for now)."""
    return []


async def delete_all_memories() -> bool:
    """Delete all memories (stub — not implemented for safety)."""
    logger.warning("delete_all_memories called but not implemented")
    return False


async def prewarm() -> None:
    """No-op — RAG initializes on first use."""
