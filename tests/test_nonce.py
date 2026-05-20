"""Tests for NonceGenerator."""

import re

from muzzle.nonce import NonceGenerator


class TestNonceGenerator:
    def test_default_length(self):
        gen = NonceGenerator()
        assert len(gen.current) == 16  # 8 bytes = 16 hex chars

    def test_custom_length(self):
        gen = NonceGenerator(byte_length=12)
        assert len(gen.current) == 24

    def test_hex_only(self):
        gen = NonceGenerator()
        assert re.fullmatch(r"[0-9a-f]+", gen.current)

    def test_minimum_byte_length(self):
        import pytest
        with pytest.raises(ValueError):
            NonceGenerator(byte_length=2)
        NonceGenerator(byte_length=4)

    def test_regenerate_changes_nonce(self):
        gen = NonceGenerator()
        first = gen.current
        second = gen.regenerate()
        assert second != first
        assert gen.current == second

    def test_tag_name_format(self):
        gen = NonceGenerator()
        assert gen.tag_name == f"tool_output_{gen.current}"

    def test_open_close_tags(self):
        gen = NonceGenerator()
        nonce = gen.current
        assert gen.open_tag == f"<tool_output_{nonce}>"
        assert gen.close_tag == f"</tool_output_{nonce}>"

    def test_tags_update_after_regenerate(self):
        gen = NonceGenerator()
        old_close = gen.close_tag
        gen.regenerate()
        assert gen.close_tag != old_close

    def test_uniqueness_across_instances(self):
        nonces = {NonceGenerator().current for _ in range(50)}
        assert len(nonces) == 50
