# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**cospec** is a collaborative specification CLI platform where humans and AI agents work together to build high-quality software. It follows a "Doc-as-Context" and "Consistency-First" philosophy, ensuring code reflects specifications and decisions are made through clear trade-off analysis.

**Core Philosophy:**
- **Codebase as Context**: Documentation is the ground truth
- **Consistency First**: Eliminate discrepancies between docs and code before implementation
- **Decision Support**: AI provides options with Pros/Cons to support human decision-making

## Commands

### Essential Development Commands

```bash
# Setup and environment
task setup              # Setup virtual environment and dependencies
source venv/bin/activate # Activate virtual environment

# Development workflow
task check              # Run all checks (lint + type-check + test) - MUST PASS before committing
task test               # Run tests
task lint               # Run linters (ruff check and format)
task lint-fix           # Run linters and fix issues
task type-check         # Run type checking (mypy)

# Testing individual components
pytest                  # Run all tests
pytest -xvs             # Stop on first failure with verbose output
pytest tests/test_file.py -xvs  # Run specific test file

# Clean up
task clean              # Clean temporary files and caches
```

### cospec CLI Commands

```bash
# Initialize a new project with recommended structure
cospec init

# Review codebase consistency against documentation
cospec review --tool Qwen       # Use Qwen (default)
cospec review --tool Opencode   # Use Opencode

# Check project status
cospec status
```

### Build and Package

```bash
# Install package in development mode
pip install -e ".[dev]"

# Build package
python -m build
```

## Code Architecture

### Project Structure

```
cospec/
├── src/cospec/                # Main package
│   ├── main.py              # CLI entry point (typer)
│   ├── agents/              # AI agent implementations
│   │   ├── base.py          # BaseAgent class
│   │   └── reviewer.py      # ReviewerAgent for code reviews
│   ├── core/                # Core functionality
│   │   ├── analyzer.py      # ProjectAnalyzer for context collection
│   │   └── config.py        # Configuration management (pydantic-settings)
│   └── __init__.py
├── docs/                    # Project documentation and specifications
│   ├── SPEC.md             # Functional requirements
│   ├── BLUEPRINT.md        # Technical architecture
│   ├── PLAN.md             # Implementation plans
│   ├── WorkingLog.md       # Development history
│   └── Overview*.md        # Guidelines and best practices
├── tests/                   # Test suite (pytest)
├── Taskfile.yml            # Task automation (go-task)
└── pyproject.toml          # Python project configuration
```

### Key Classes and Architecture

**Core Components:**
- `main.py`: Typer-based CLI with `init`, `review`, and `status` commands
- `BaseAgent`: Base class for AI agent implementations with tool execution
- `ReviewerAgent`: Specialized agent for code review using external tools
- `ProjectAnalyzer`: Collects project context from docs and source code
- `CospecConfig`: Configuration management with tool settings and language preferences

**Agent Architecture:**
- External tool integration (Qwen, Opencode, Crush, MistralVibe, Gemini-CLI)
- Language-aware prompting (Japanese/English support)
- Context collection from docs/ directory and source code

## Development Guidelines

### Code Quality Standards

**Type Safety:**
- Use Pydantic models for data structures
- Avoid `Any` types - prefer specific type annotations
- Use strong typing throughout the codebase

**Documentation:**
- Write docstrings before implementation
- Update SPEC.md when adding new features
- Maintain BLUEPRINT.md for technical decisions

**Testing:**
- Follow Test-Driven Generation (TDG) approach
- Mock external dependencies (HTTP, APIs)
- Use pytest with async support

### External Dependencies

**Required Tools:**
- AI-Agent CLI tools (Qwen, Opencode, Crush, MistralVibe, Gemini-CLI) for integration
- `go-task` for task automation (optional but recommended)

**Python Dependencies:**
- `typer>=0.9.0` - CLI framework
- `rich>=13.0.0` - Rich terminal output
- `pydantic-settings>=2.0.0` - Configuration management
- `openai>=1.0.0` - OpenAI API client
- `pytest>=7.0.0` - Testing framework

### Configuration

**Environment Variables:**
- `COSPEC_LANGUAGE`: Language for AI responses (`ja` or `en`, default: `ja`)
- `COSPEC_DEFAULT_TOOL`: Default tool for reviews (default: `Qwen`)

**Configuration File:**
- Configuration managed via `CospecConfig` class
- Tool settings defined in `pyproject.toml` or environment variables

### Development Workflow

1. **Setup**: Run `task setup` to create virtual environment and install dependencies
2. **Development**: Use `task check` to validate changes before committing
3. **Testing**: Write tests before implementation when possible
4. **Linting**: Use `task lint-fix` to automatically fix code style issues
5. **Review**: Use `cospec review` to check consistency with documentation

### Important Files

- `docs/SPEC.md` - Functional requirements (the "What")
- `docs/BLUEPRINT.md` - Technical architecture (the "How")
- `.rules/OverviewBasicRule.md` - Human-AI協働開発の実践ワークフロー
- `.rules/OverviewCodingTestingThinking.md` - Coding and testing guidelines
- `.rules/OverviewDesignThinking.md` - Design philosophy and patterns
- `docs/PLAN.md` - Implementation checklists
- `docs/WorkingLog.md` - Development history

## Testing Strategy

**Test Structure:**
- Tests located in `/tests/` directory
- Use pytest with `-xvs` flags for debugging
- Mock external dependencies using pytest-mock
- Async test support with pytest-asyncio

**Test Commands:**
```bash
pytest                  # Run all tests
pytest -xvs             # Stop on first failure with verbose output
pytest tests/           # Run all tests in tests directory
pytest tests/test_main.py -xvs  # Run specific test file
```

**Test Best Practices:**
- Mock external API calls
- Test CLI commands with typer testing utilities
- Use dependency injection for testability
- Follow TDG (Test-Driven Generation) approach

## Common Development Tasks

### Adding a New CLI Command
1. Add command to `src/cospec/main.py`
2. Update SPEC.md if it's a user-facing feature
3. Write tests in `tests/` directory
4. Run `task check` to validate

### Adding a New AI Agent
1. Create new agent class in `src/cospec/agents/`
2. Inherit from `BaseAgent`
3. Implement specific functionality
4. Update tool configuration if needed

### Modifying Configuration
1. Update `CospecConfig` class in `src/cospec/core/config.py`
2. Add environment variable support if needed
3. Update tests for configuration changes

## Communication Guidelines

**Language Policy:**
- **User Interaction**: All conversations with the user are conducted in Japanese
- **Code Comments**: Source code comments and documentation should be in English
- **Commit Messages**: Use English for commit messages to maintain consistency with the codebase
- **Documentation**: docs/以下の *.md は、既に日本語のものは継続して日本語で記述する

**Note**: This policy ensures that while user communication remains in Japanese for clarity, the codebase maintains international standards with English comments and documentation.

## Troubleshooting

**Common Issues:**
- `ModuleNotFoundError`: Ensure virtual environment is activated
- `task: command not found`: Install go-task or use Python commands directly
- External tool errors: Verify AI-Agent CLI tools (Qwen, Opencode, etc.) are installed and in PATH


**Debug Commands:**
```bash
# Check Python path and environment
python -c "import sys; print(sys.path)"

# Verify tool installations
which qwen          # For Qwen
which opencode      # For Opencode
which crush         # For Crush
which vibe          # For MistralVibe
which gemini        # For Gemini-CLI

# Run individual checks
ruff check src/cospec/
mypy src/cospec/
```