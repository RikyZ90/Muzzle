"""Muzzle — Randomized Tool Output Wrapping.

Anti-prompt-injection defense for LLM agent tool outputs.
Extracted from the ShibaClaw security architecture.
"""

from __future__ import annotations

from muzzle.formatter import SystemPromptFormatter
from muzzle.nonce import NonceGenerator
from muzzle.sanitizer import OutputSanitizer

__all__ = [
    "NonceGenerator",
    "OutputSanitizer",
    "SystemPromptFormatter",
    "wrap_tool_output",
]

_default_nonce: NonceGenerator | None = None


def wrap_tool_output(
    text: str,
    tool_name: str,
    *,
    nonce: NonceGenerator | None = None,
    is_risky: bool = False,
) -> str:
    """Convenience wrapper: sanitize and wrap a tool output in one call.

    If no *nonce* is provided, an internal default ``NonceGenerator`` is
    created (and reused across calls).  Call ``nonce.regenerate()`` between
    agent loop iterations to rotate the delimiter.
    """
    global _default_nonce
    if nonce is None:
        if _default_nonce is None:
            _default_nonce = NonceGenerator()
        nonce = _default_nonce
    return OutputSanitizer.wrap(text, nonce, tool_name, is_risky=is_risky)
