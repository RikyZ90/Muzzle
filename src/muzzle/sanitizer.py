"""Sanitization and wrapping of tool outputs against prompt injection."""

from __future__ import annotations

from muzzle.nonce import NonceGenerator
import base64

_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "you are now",
    "system prompt",
]



class OutputSanitizer:
    """Sanitizes and wraps tool output to prevent delimiter escape attacks.

    Any occurrence of the current closing tag inside the tool output is escaped
    so the LLM cannot be tricked into treating injected text as the end of the
    trusted tool-output block.
    """

    @staticmethod
    def pre_scan(text: str) -> str:
        text_lower = text.lower()
        for pattern in _INJECTION_PATTERNS:
            if pattern in text_lower:
                return "[SECURITY WARNING: Potential Prompt Injection Detected. Content sanitized.]"
        return text

    @staticmethod
    def sanitize(text: str, nonce: NonceGenerator) -> str:
        """Escape closing-tag sequences that appear in *text*."""
        closing = nonce.close_tag
        escaped = closing.replace("</", "<\\/")
        return text.replace(closing, escaped)

    @staticmethod
    def wrap(text: str, nonce: NonceGenerator, tool_name: str, *, is_risky: bool = False) -> str:
        """Sanitize *text* and wrap it in randomized delimiters.

        Returns a string ready to be used as the ``content`` field of a
        ``role=tool`` message in the LLM conversation.
        """
        text = OutputSanitizer.pre_scan(text)
        tag = nonce.tag_name
        
        if is_risky:
            encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
            return f'<{tag} encoding="base64" name="{tool_name}">\n{encoded}\n</{tag}>'
            
        sanitized = OutputSanitizer.sanitize(text, nonce)
        return f'<{tag} name="{tool_name}">\n{sanitized}\n</{tag}>'
