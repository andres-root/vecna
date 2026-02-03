"""File read tool - safely reads files from the working directory."""

from pathlib import Path
from typing import Any

from vecna.tools.exceptions import PathSecurityError
from vecna.tools.utils import format_file_contents, validate_path


class FileReadTool:
    """Tool for reading files from the working directory.

    Security:
    - Only reads files within the working directory
    - Validates paths to prevent traversal attacks
    """

    def __init__(self, working_dir: Path) -> None:
        """Initialize with the working directory.

        Args:
            working_dir: The directory to restrict file access to.
        """
        self.working_dir = working_dir.resolve()

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return (
            "Read the contents of a file at the specified path. "
            "The path must be relative to the working directory."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": (
                        "Path to the file to read, relative to working directory. "
                        "Example: 'src/main.py' or 'README.md'"
                    ),
                }
            },
            "required": ["path"],
        }

    def execute(self, path: str) -> str:
        """Read a file and return its contents.

        Args:
            path: Path to the file (relative to working directory).

        Returns:
            Formatted file contents with line numbers, or an error message.
        """
        try:
            # Validate the path
            resolved_path = validate_path(path, self.working_dir)

            # Check if file exists
            if not resolved_path.exists():
                return f"Error: File not found: {path}"

            # Check if it's actually a file
            if not resolved_path.is_file():
                return f"Error: Not a file: {path}"

            # Read the file
            contents = resolved_path.read_text()

            # Format and return
            return format_file_contents(resolved_path.name, contents)

        except PathSecurityError as e:
            return str(e)
        except PermissionError:
            return f"Error: Permission denied: {path}"
        except UnicodeDecodeError:
            return f"Error: Cannot read binary file: {path}"
        except Exception as e:
            return f"Error reading file: {e}"
