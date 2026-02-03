"""UI utilities for terminal output using Rick."""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.theme import Theme

# Create a custom theme for consisten styling
custom_theme = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "red bold",
        "success": "green",
        "prompt": "blue bold",
    }
)

# Global console instance
console = Console(theme=custom_theme)


def print_welcome() -> None:
    """Print the welcome message."""
    console.print()
    console.print("[bold blue]Vecna[/bold blue] v0.1.0 - AI Coding Assistant")
    console.print("[dim]Type 'exit' to quit[/dim]")
    console.print()


def print_response(text: str) -> None:
    """Print an assistant response with markdown formatting."""
    md = Markdown(text)
    console.print(md)
    console.print()


def print_help() -> None:
    """Print help information."""
    help_text = """
    ## Commands

    - **exit** or **quit**: Exit Vecna
    - **help**: Show this help message
    - **clear**: Clear the screen

    ## Usage

    Just type your request and press Enter. For example:
    - "Read the main.py file"
    - "Add type hints to the greet function"
    """
    print_response(help_text)


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[error]Error:[/error] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[success]✓[/success] {message}")


def print_tool_call(tool_name: str, args: dict) -> None:
    """Print a tool invocation."""
    args_str = ", ".join(f'{k}="{v}"' for k, v in args.items())
    console.print(f"[dim]→ {tool_name}({args_str})[/dim]")


def print_tool_result(result: str, success: bool = True) -> None:
    """Print a tool result in a panel."""
    style = "green" if success else "red"
    console.print(Panel(result, border_style=style, padding=(0, 1)))


def get_prompt() -> str:
    """Get the input prompt string."""
    return "[prompt]>[/prompt] "
