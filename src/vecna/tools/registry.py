"""Tool registry - manages tool registration and execution."""

from typing import Any

from vecna.tools.base import Tool, tool_to_anthropic_format


class ToolRegistry:
    """Registry that holds all available tools.

    The registry:
    - Stores tools by name for quick lookup
    - Converts tools to API format
    - Executes tool calls
    """

    def __init__(self) -> None:
        """Initialize an empty registry."""
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a tool.

        Args:
            tool: The tool to register.
        """
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        """Get a tool by name.

        Args:
            name: The tool's name.

        Returns:
            The tool, or None if not found.
        """
        return self._tools.get(name)

    def to_anthropic_format(self) -> list[dict[str, Any]]:
        """Convert all tools to Anthropic API format.

        Returns:
            List of tool definitions for the API.
        """
        return [tool_to_anthropic_format(tool) for tool in self._tools.values()]

    def execute(self, name: str, arguments: dict[str, Any]) -> str:
        """Execute a tool by name with arguments.

        Args:
            name: The tool's name.
            arguments: The arguments to pass to the tool.

        Returns:
            The tool's result as a string.

        Raises:
            ValueError: If the tool is not found.
        """
        tool = self.get(name)
        if tool is None:
            return f"Error: unknown tool'{name}'"

        try:
            return tool.execute(**arguments)
        except Exception as e:
            return f"Error executing {name}: {e}"

    def list_tools(self) -> list[str]:
        """List all registered tool names."""
        return list(self._tools.keys())
