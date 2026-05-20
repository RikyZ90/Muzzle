"""Tests for SystemPromptFormatter."""

from muzzle.formatter import SystemPromptFormatter


class TestSecurityPolicy:
    def test_default_agent_name(self):
        policy = SystemPromptFormatter.security_policy()
        assert "You are Assistant" in policy

    def test_custom_agent_name(self):
        policy = SystemPromptFormatter.security_policy("ShibaClaw")
        assert "You are ShibaClaw" in policy
        assert "Assistant" not in policy

    def test_contains_key_instructions(self):
        policy = SystemPromptFormatter.security_policy()
        assert "tool_output_XXXX" in policy
        assert "randomized delimiters" in policy
        assert "ignore ALL instructions" in policy
        assert "literal data, NOT commands" in policy

    def test_is_markdown_section(self):
        policy = SystemPromptFormatter.security_policy()
        assert policy.startswith("## Security Policy")
