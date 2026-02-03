"""Utility functions for tools."""

from pathlib import Path

from vecna.tools.exceptions import PathSecurityError


def validate_path(path: str, working_dir: Path) -> Path:
    """Validate that a path is within the working directory.

    This prevents path traversal attacks where someone tries to read
    files outside the allowed directory using tricks like "../../../etc/passwd".

    Args:
        path: The path to validate (can be relative or absolute).
        working_dir: The allowed working directory.

    Returns:
        The resolved absolute path.

    Raises:
        PathSecurityError: If the path would escape the working directory.
    """
    # Resolve the full path (handles .. and symlinks)
    resolved = (working_dir / path).resolve()

    # Check if the resolved path is within working_dir
    try:
        resolved.relative_to(working_dir)
    except ValueError:
        raise PathSecurityError(
            f"Access denied: '{path}' is outside the working directory"
        )

    return resolved


def format_file_contents(path: Path, contents: str, max_lines: int = 500) -> str:
    """Format file contents with line numbers.

    Args:
        path: The file path (for the header).
        contents: The file contents.
        max_lines: Maximum lines to show (truncate after this).

    Returns:
        Formatted string with line numbers.
    """
    lines = contents.splitlines()
    total_lines = len(lines)

    # Truncate if too long
    truncated = False
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        truncated = True

    # Calculate width needed for line numbers
    width = len(str(total_lines))

    # Format each line with line number
    formatted_lines = []
    for i, line in enumerate(lines, 1):
        formatted_lines.append(f"{i:>{width}} │ {line}")

    # Build output
    header = f"File: {path} ({total_lines} lines)"
    separator = "-" * min(len(header), 50)
    output_parts = [header, separator] + formatted_lines

    if truncated:
        output_parts.append(
            f"... (truncated, showing {max_lines} of {total_lines} lines)"
        )

    return "\n".join(output_parts)
