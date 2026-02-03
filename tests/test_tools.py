"""Tests for the tools system."""

from vecna.tools import ToolRegistry
from vecna.tools.echo import EchoTool


def test_tool_registry_register_and_get():
    """Test that we can register and retrieve a tool."""
    registry = ToolRegistry()
    echo_tool = EchoTool()
    registry.register(echo_tool)
    assert registry.get("echo") is echo_tool
    assert registry.get("nonexistent") is None


def test_tool_registry_execute():
    """Test that we can execute a tool through the registry."""
    registry = ToolRegistry()
    echo_tool = EchoTool()
    registry.register(echo_tool)
    result = registry.execute("echo", {"message": "Hello!"})
    assert result == "Echo: Hello!"


def test_tool_to_anthropic_format():
    """Test conversion to Anthropic API format."""
    registry = ToolRegistry()
    echo_tool = EchoTool()
    registry.register(echo_tool)
    tools = registry.to_anthropic_format()
    assert len(tools) == 1
    assert tools[0]["name"] == "echo"
    assert "input_schema" in tools[0]
