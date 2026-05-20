"""Nonce generation for randomized tool output delimiters."""

from __future__ import annotations

import secrets

_MIN_BYTE_LENGTH = 4


class NonceGenerator:
    """Generates and manages cryptographic nonces for tool output wrapping.

    Each nonce produces a unique XML-style tag pair used to delimit tool outputs,
    making it impossible for injected content to predict or forge the closing tag.
    """

    def __init__(self, byte_length: int = 8) -> None:
        if byte_length < _MIN_BYTE_LENGTH:
            raise ValueError(
                f"byte_length must be >= {_MIN_BYTE_LENGTH} (got {byte_length}); "
                f"lower values don't provide enough entropy"
            )
        self._byte_length = byte_length
        self._nonce = secrets.token_hex(byte_length)

    @property
    def current(self) -> str:
        return self._nonce

    def regenerate(self) -> str:
        self._nonce = secrets.token_hex(self._byte_length)
        return self._nonce

    @property
    def tag_name(self) -> str:
        return f"tool_output_{self._nonce}"

    @property
    def open_tag(self) -> str:
        return f"<{self.tag_name}>"

    @property
    def close_tag(self) -> str:
        return f"</{self.tag_name}>"
