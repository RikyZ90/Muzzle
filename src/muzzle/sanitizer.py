"""Sanitization and wrapping of tool outputs against prompt injection."""

from __future__ import annotations

from muzzle.nonce import NonceGenerator


class OutputSanitizer:
    """Sanitizes and wraps tool output to prevent delimiter escape attacks.

    Any occurrence of the current closing tag inside the tool output is escaped
    so the LLM cannot be tricked into treating injected text as the end of the
    trusted tool-output block.
    """

    @staticmethod
    def sanitize(text: str, nonce: NonceGenerator) -> str:
        """Escape closing-tag sequences that appear in *text*."""
        closing = nonce.close_tag
        escaped = closing.replace("</", "<\\/")
        return text.replace(closing, escaped)

    @staticmethod
    def wrap(text: str, nonce: NonceGenerator, tool_name: str) -> str:
        """Sanitize *text* and wrap it in randomized delimiters.

        Returns a string ready to be used as the ``content`` field of a
        ``role=tool`` message in the LLM conversation.
        """
        tag = nonce.tag_name
        sanitized = OutputSanitizer.sanitize(text, nonce)
        return f'<{tag} name="{tool_name}">\n{sanitized}\n</{tag}>'
