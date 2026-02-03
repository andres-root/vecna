"""Tests for the tools system."""

from pathlib import Path

import pytest

from vecna.tools import ToolRegistry
from vecna.tools.echo import EchoTool
from vecna.tools.exceptions import PathSecurityError
from vecna.tools.file_read import FileReadTool
from vecna.tools.utils import validate_path


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


# === Path Validation Tests ===


def test_validate_path_valid(tmp_path: Path):
    """Test that valid paths within working directory are allowed."""
    # Create a test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")

    result = validate_path("test.txt", tmp_path)

    assert result == test_file


def test_validate_path_subdirectory(tmp_path: Path):
    """Test that paths in subdirectories work."""
    # Create a subdirectory with a file
    subdir = tmp_path / "src"
    subdir.mkdir()
    test_file = subdir / "main.py"
    test_file.write_text("print('hello')")

    result = validate_path("src/main.py", tmp_path)

    assert result == test_file


def test_validate_path_traversal_blocked(tmp_path: Path):
    """Test that path traversal attempts are blocked."""
    with pytest.raises(PathSecurityError) as exc_info:
        validate_path("../../../etc/passwd", tmp_path)

    assert "outside the working directory" in str(exc_info.value)


def test_validate_path_absolute_outside_blocked(tmp_path: Path):
    """Test that absolute paths outside working dir are blocked."""
    with pytest.raises(PathSecurityError):
        validate_path("/etc/passwd", tmp_path)


# === File Read Tool Tests ===


def test_file_read_tool_success(tmp_path: Path):
    """Test reading a file successfully."""
    # Create a test file
    test_file = tmp_path / "hello.txt"
    test_file.write_text("Hello, World!\nLine 2")

    tool = FileReadTool(working_dir=tmp_path)
    result = tool.execute(path="hello.txt")

    assert "Hello, World!" in result
    assert "Line 2" in result
    assert "2 lines" in result  # Line count in header


def test_file_read_tool_not_found(tmp_path: Path):
    """Test reading a nonexistent file."""
    tool = FileReadTool(working_dir=tmp_path)
    result = tool.execute(path="nonexistent.txt")

    assert "Error: File not found" in result


def test_file_read_tool_path_traversal(tmp_path: Path):
    """Test that path traversal is blocked."""
    tool = FileReadTool(working_dir=tmp_path)
    result = tool.execute(path="../../../etc/passwd")

    assert "Access denied" in result


def test_file_read_tool_in_registry(tmp_path: Path):
    """Test that the file read tool works in the registry."""
    # Create a test file
    test_file = tmp_path / "test.py"
    test_file.write_text("x = 1")

    registry = ToolRegistry()
    registry.register(FileReadTool(working_dir=tmp_path))

    result = registry.execute("read_file", {"path": "test.py"})

    assert "x = 1" in result
