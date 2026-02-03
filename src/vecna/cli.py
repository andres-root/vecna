"""
CLI entry point for the Vecna agent.
"""

import os
from pathlib import Path

from rich.live import Live
from rich.markdown import Markdown

from vecna.agent import Agent
from vecna.ui import (
    console,
    print_error,
    print_help,
    print_welcome,
)


def main() -> None:
    """Main entry point for the Vecna CLI."""

    # Get working directory
    working_dir = Path.cwd()

    print_welcome()
    console.print(f"[dim]Working directory: {working_dir}[/dim]")
    console.print()

    # Initialize the agent
    try:
        agent = Agent()
    except ValueError as e:
        print_error(str(e))
        return

    while True:
        try:
            # Show prompt and get input
            user_input = console.input("[blue bold]>[/blue bold] ")

            # Skip empty lines
            if not user_input.strip():
                continue

            # Handle built-in commands
            command = user_input.strip().lower()

            # Check for exit command
            if command in ("exit", "quit"):
                console.print("[dim]Goodbye![/dim]")
                break

            if command == "help":
                print_help()
                continue

            if command == "clear":
                os.system("clear" if os.name != "nt" else "cls")
                print_welcome()
                continue

            # Streamed response from model's API
            console.print()  # Add spacing

            full_response = ""
            # Use Live to update display as text streams in
            with Live(Markdown(""), console=console, refresh_per_second=10) as live:
                for chunk in agent.chat_stream(user_input):
                    full_response += chunk
                    # Echo the response
                    live.update(Markdown(full_response))

            console.print()  # Add spacing
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            console.print("\n[dim]Goodbye![/dim]")
            break

        except EOFError:
            # Handle Ctrl+D (end of input)
            console.print("\n[dim]Goodbye![/dim]")
            break


if __name__ == "__main__":
    main()
