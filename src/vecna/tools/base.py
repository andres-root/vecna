"""
Base classes for tools
"""

from typing import Any, Protocol


class Tool(Protocol):
    """Protocol that all tools must follow.

    A tool has:
    - name: Unique identifier (e.g., "read_file")
    - description: What it does (shown to Claude)
    - parameters: JSON Schema describing the inputs
    - execute(): Method that performs the action
    """

    @property
    def name(self) -> str:
        """Tool name"""
        pass

    @property
    def description(self) -> str:
        """Tool description"""
        pass

    @property
    def parameters(self) -> dict[str, Any]:
        """JSON Schema for the tool's parameters"""
        pass

    def execute(self, **kwargs: Any) -> str:
        """Execute the tool with the given arguments

        Args:
            **kwargs: The parameters defined in the schema

        Returns:
            A string result to show to the LLM.
        """
        pass


def tool_to_anthropic_format(tool: Tool) -> dict[str, Any]:
    """Convert a tool to Anthropic API format.

    Anthropic expects tools in this format:
    {
        "name": "tool_name",
        "description": "What it does",
        "input_schema": { JSON Schema }
    }
    """
    return {
        "name": tool.name,
        "description": tool.description,
        "input_schema": tool.parameters,
    }
