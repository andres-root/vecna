"""Utility functions for Vecna."""

import os

from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_client() -> Anthropic:
    """Create and return an Anthropic client.

    Raises:
        ValueError: If ANTHROPIC_API_KEY is not set.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is not set.\n"
            "Get your API key from: https://console.anthropic.com/\n"
            "Then add it to your .env file: ANTHROPIC_API_KEY=sk-ant-..."
        )

    return Anthropic(api_key=api_key)
