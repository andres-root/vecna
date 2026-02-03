"""Echo tool - a simple test tool that echoes input."""

from typing import Any


class EchoTool:
    """A simple tool that echoes back its input.

    This is useful for testing the tool system.
    """

    @property
    def name(self) -> str:
        return "echo"

    @property
    def description(self) -> str:
        return "Echoes back the provided message. Useful for testing."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "The message to echo back"}
            },
            "required": ["message"],
        }

    def execute(self, message: str) -> str:
        """Echo the message back.

        Args:
            message: The message to echo.

        Returns:
            The same message.
        """
        return f"Echo: {message}"
