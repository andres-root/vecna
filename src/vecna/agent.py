"""Agent - Core logic for interacting with Claude."""

import os

from vecna.prompts import SYSTEM_PROMPT
from vecna.utils import get_client


class Agent:
    """The main agent that handles conversations with Claude."""

    def __init__(self) -> None:
        """Initialize the agent."""
        self.client = get_client()
        self.model = os.environ.get("VECNA_MODEL", "claude-sonnet-4-5-20250929")
        self.max_tokens = os.environ.get("VECNA_MAX_TOKENS", 1024)
        self.messages: list[dict] = []

    def chat(self, user_message: str) -> str:
        """Send a message and get a response.

        Args:
            user_message: The user's input.

        Returns:
            The assistant's response text.
        """

        # Add user message to history
        self.messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        # Call the API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=int(self.max_tokens),
            system=SYSTEM_PROMPT,
            messages=self.messages,
        )

        # Extract the response text
        assistant_message = response.content[0].text

        # Add assistant message to history
        self.messages.append(
            {
                "role": "assistant",
                "content": assistant_message,
            }
        )

        return assistant_message

    def chat_stream(self, user_message: str) -> str:
        """Send a message and stream the response.

        Args:
            user_message: The user's input.

        Yields:
            Chunks of the response text as they arrive.
        """
        self.messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        # To collect the full response for history
        full_response = ""

        # Use streaming API
        with self.client.messages.stream(
            model=self.model,
            max_tokens=8096,
            system=SYSTEM_PROMPT,
            messages=self.messages,
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                yield text

        # Add complete response to history
        self.messages.append({"role": "assistant", "content": full_response})
