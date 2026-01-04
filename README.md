# cospec

**Collaborative Specification CLI** - A platform where humans and AI agents work together to build high-quality software.

`cospec` follows a **"Doc-as-Context"** and **"Consistency-First"** philosophy. It ensures that your code reflects your specifications and that decisions are made through clear trade-off analysis.

## Core Concepts

- **Codebase as Context**: Documentation is the ground truth.
- **Consistency First**: Eliminate discrepancies between docs and code before implementation.
- **Decision Support**: AI provides options with Pros/Cons to support human decision-making.

## Key Features

### Implemented
- **`cospec init`**: Initialize a new project with the recommended structure (`docs/`, `Taskfile.yml`) and guideline files.
- **`cospec review`**: Analyze the codebase for inconsistencies using external AI tools (e.g., `qwen`, `opencode`).

### Planned
- **`cospec hear`**: Interactive hearing to resolve ambiguities in `SPEC.md`.
- **`cospec test-gen`**: Generate test cases from specifications (Test-Driven Generation).

## Architecture

`cospec` acts as an orchestrator for AI coding agents. Instead of embedding a heavy LLM runtime, it delegates intelligence to installed CLI tools (Agentic Coding Tools).

- **Current Integrations**: `qwen` (Qwen Code), `opencode`.
- **Context Awareness**: `cospec` automatically gathers relevant context (Docs + Code) to construct effective prompts for these tools.

## Getting Started

### Prerequisites

- Python 3.10+
- [go-task](https://taskfile.dev/) (optional, but recommended)
- External Tools: Ensure `qwen` or `opencode` is installed and available in your PATH.

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/your-org/cospec.git
cd cospec

# Setup environment (creates venv and installs dependencies)
task setup
```

### Usage

#### 1. Initialize a Project
```bash
cospec init
```
This creates a `docs/` directory with templates for specifications and guidelines (`OverviewCodingTestingThinking.md`).

#### 2. Review Code Consistency
```bash
# Use Qwen Code (default)
cospec review --tool qwen

# Use OpenCode
cospec review --tool opencode
```
The agent will analyze your `docs/` and `src/` files and generate a Markdown report in `docs/review_YYYYMMDD_...`.

## Configuration

You can configure `cospec` via environment variables (e.g., `.env` file).

| Variable | Default | Description |
|----------|---------|-------------|
| `COSPEC_LANGUAGE` | `ja` | Language for AI responses (`ja`, `en`). |
| `COSPEC_DEFAULT_TOOL` | `qwen` | Default tool to use for review. |

## Development

See [GEMINI.md](./GEMINI.md) for agent instructions and [docs/](./docs/) for detailed specifications.

- `task test`: Run tests
- `task lint`: Run linters
- `task check`: Run all checks

## License

MIT