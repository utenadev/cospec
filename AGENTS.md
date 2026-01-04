# AGENTS.md - Guidelines for Agentic Coding

This file provides guidance for AI agents working on the cospec repository.

## Build/Lint/Test Commands

### Essential Commands
```bash
# Setup environment
task setup              # Create venv and install dependencies
source venv/bin/activate # Activate virtual environment

# Run all checks (MUST PASS before committing)
task check              # Lint + Type-check + Test

# Individual checks
task test               # Run all tests
pytest                  # Alias for task test
pytest -xvs             # Stop on first failure with verbose output
pytest tests/test_file.py -xvs  # Run specific test file with verbose output
pytest tests/           # Run all tests in tests directory

task lint               # Run ruff check and format check
task lint-fix           # Auto-fix linting issues and format code
task type-check         # Run mypy type checking
task docs:check         # Check documentation consistency
task quality:check      # Comprehensive quality check (lint + type-check + test + docs:check)

# Clean up
task clean              # Remove venv, caches, and temporary files
```

### CLI Commands
```bash
cospec init             # Initialize project with recommended structure
cospec review --tool Qwen       # Review codebase consistency (Qwen default)
cospec review --tool Opencode   # Review using opencode
cospec hear --tool Qwen         # Clarify ambiguous requirements
cospec test-gen --tool Qwen     # Generate test cases from specifications
cospec status           # Show project status

# Agent management
cospec agent list       # List all registered AI-Agents
cospec agent add <name> --command <command>  # Add new AI-Agent (auto-analyzes --help)
cospec agent test <name>  # Test a registered AI-Agent
```

### Tool Selection Logic
- **hear, test-gen**: Uses `COSPEC_DEV_TOOL` environment variable if set, otherwise uses `default_tool`
- **review**: Randomly selects 2 different AI-Agents (excluding dev_tool) for diverse review

## Code Style Guidelines

### Imports
- Use absolute imports from the `cospec` package
- Group imports: standard library, third-party, local
- Use `from typing import Optional, Dict, List` for common types
- Keep imports at the top of files

### Formatting
- **Line length**: 120 characters (configured in ruff)
- Use `ruff format` for code formatting
- Run `task lint-fix` before committing

### Types
- **Strong typing required**: Use Pydantic models for data structures
- **NO `Any` types**: Always use specific type annotations
- Use type hints for all function parameters and return values
- Use `Optional[T]` for nullable values, not `T | None` consistently (stick to one style)

### Naming Conventions
- **Classes**: PascalCase (e.g., `BaseAgent`, `ReviewerAgent`, `CospecConfig`)
- **Functions/Methods**: snake_case (e.g., `run_tool`, `review_project`, `load_config`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_RETRIES`)
- **Private methods**: single underscore prefix (e.g., `_build_prompt`)
- **Test functions**: test_ prefix with descriptive names (e.g., `test_extract_unclear_points`)

### Documentation
- **Write docstrings before implementation** (Test-Driven Generation approach)
- Use Google-style or Sphinx-style docstrings
- Describe parameters, returns, and raises sections
- Include examples for complex functions

### Error Handling
- Use specific exception types (ValueError, RuntimeError, etc.)
- Include descriptive error messages
- Use `raise ... from e` for exception chaining
- Wrap subprocess calls in try-except blocks
- Use typer.Exit for CLI errors

### Testing Strategy (Test-Driven Generation - TDG)
1. **Scaffold**: Agree on test scenarios with user
2. **Test Generation**: Write failing tests (Red) first
3. **Implementation**: Write minimal code to pass tests (Green)
4. **Refactoring**: Clean up while maintaining passing tests

**Mocking**:
- Mock all external I/O (HTTP, APIs, file system in tests)
- Use `pytest-mock` for mocking
- Use dependency injection for testability
- External tools (`Qwen`, `Opencode`, etc.) should be mocked in tests

### Configuration
- Use `pydantic-settings` for configuration management
- Environment variables use `COSPEC_` prefix
- Default values should be reasonable for development
- Tool configuration in `CospecConfig.tools` dict

### Project Structure
```
src/cospec/
├── main.py              # CLI entry point (typer)
├── agents/              # AI agent implementations
│   ├── base.py          # BaseAgent class
│   ├── reviewer.py      # ReviewerAgent
│   ├── hearer.py        # HearerAgent
│   └── test_generator.py # TestGeneratorAgent
├── core/                # Core functionality
│   ├── analyzer.py      # ProjectAnalyzer
│   └── config.py        # CospecConfig
└── __init__.py
tests/                   # pytest test files
docs/                    # Documentation (ground truth)
```

### Development Workflow
1. Read existing code to understand patterns before making changes
2. Use `task lint-fix` to format code automatically
3. Run `task check` before committing (all checks must pass)
4. Update documentation (SPEC.md, BLUEPRINT.md) when adding features
5. Follow Test-Driven Generation: write tests, then implement
6. Avoid adding comments unless explicitly asked - code should be self-documenting

### Pre-commit Requirements
Before declaring work complete, agents MUST:
1. Run `task check` - all checks must pass
2. Ensure all tests pass
3. Verify no linting errors remain
4. Confirm type checking passes
5. Only then should work be considered complete

### Language Policy
- **User communication**: Japanese
- **Code comments**: English
- **Commit messages**: English
- **Documentation**: docs/以下の *.md は、既に日本語のものは継続して日本語で記述する

### Key Files to Reference
- `docs/SPEC.md` - Functional requirements
- `docs/BLUEPRINT.md` - Technical architecture
- `docs/PLAN.md` - Implementation plans
- `docs/WorkingLog.md` - Development history
- `pyproject.toml` - Project configuration and dependencies
- `.cospec/config.json` - Tool configuration

### Tool Configuration Examples

**Qwen (default)**:
```json
{
  "command": "qwen",
  "args": ["{prompt}"]
}
```

**Opencode**:
```json
{
  "command": "opencode",
  "args": ["run", "{prompt}"]
}
```

**Note**: The `{prompt}` placeholder is automatically replaced with the full prompt. For long prompts (>8000 chars), the system uses temporary files automatically.
