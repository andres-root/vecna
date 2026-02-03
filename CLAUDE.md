# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Vecna is a terminal-based AI coding assistant built in Python. It's a learning project demonstrating how to build a ReAct-style agent that interacts with Claude through the Anthropic API. Currently implements basic conversation with streaming responses; file read/edit tools are planned but not yet implemented.

## Commands

```bash
# Install dependencies (including dev tools)
uv sync --extra dev

# Run the CLI
uv run vecna

# Run tests
uv run pytest
uv run pytest tests/test_tools.py -v  # specific file

# Format and lint
uv run black src/ tests/
uv run pre-commit run --all-files

# Install pre-commit hooks (run once after cloning)
uv run pre-commit install
```

## Environment Variables

Store in `.env` file (loaded via python-dotenv):

- `ANTHROPIC_API_KEY` (required): Anthropic API key
- `VECNA_MODEL`: Model to use (default: `claude-sonnet-4-5-20250929`)
- `VECNA_MAX_TOKENS`: Max tokens per response (default: `1024`)

## Architecture

```
src/vecna/
├── cli.py          # Entry point, REPL loop with Rich Live streaming
├── agent.py        # Agent class: conversation state, API calls (chat/chat_stream)
├── utils.py        # get_client() - creates Anthropic client, loads .env
├── ui.py           # Rich-based terminal output (welcome, help, response formatting)
├── prompts/
│   └── system.py   # SYSTEM_PROMPT constant
└── tools/
    └── base.py     # Tool Protocol definition (for future tools)
```

**Current flow:**
1. `cli.py` → displays welcome, initializes Agent, runs REPL
2. User input → `agent.chat_stream()` → streams response via Anthropic API
3. Rich Live renders markdown in real-time
4. Response appended to conversation history

**Tool system (foundation only):**
- `Tool` Protocol in `tools/base.py` defines interface: `name`, `description`, `parameters`, `execute()`
- `tool_to_anthropic_format()` converts to API format
- No tools implemented yet

## Specification

See `.notes/SPEC.md` for the full project vision including planned features:
- File read/edit tools
- Context summarization
- Permission system for file writes
