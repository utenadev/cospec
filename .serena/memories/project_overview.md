# cospec Project Overview

## Purpose
cospec is a **Collaborative Specification CLI** platform where humans and AI agents work together to build high-quality software. It follows a "Doc-as-Context" and "Consistency-First" philosophy.

## Core Philosophy
- **Codebase as Context**: Documentation is the ground truth
- **Consistency First**: Eliminate discrepancies between docs and code before implementation
- **Decision Support**: AI provides options with Pros/Cons to support human decision-making

## Tech Stack
- **Language**: Python 3.10+
- **CLI Framework**: Typer (>=0.9.0)
- **Terminal Output**: Rich (>=13.0.0)
- **Configuration**: Pydantic Settings (>=2.0.0)
- **Testing**: pytest (>=7.0.0)
- **Linting**: ruff (>=0.1.0)
- **Type Checking**: mypy (>=1.0.0)

## Project Structure
```
cospec/
├── src/cospec/                # Main package
│   ├── main.py              # CLI entry point (typer)
│   ├── agents/              # AI agent implementations
│   ├── core/                # Core functionality
│   └── __init__.py
├── docs/                    # Project documentation and specifications
│   ├── SPEC.md             # Functional requirements
│   ├── BLUEPRINT.md        # Technical architecture
│   ├── PLAN.md             # Implementation plans
│   ├── WorkingLog.md       # Development history
│   └── Overview*.md        # Guidelines and best practices
├── .rules/                  # Development guidelines
├── tests/                   # Test suite (pytest)
├── Taskfile.yml            # Task automation (go-task)
└── pyproject.toml          # Python project configuration
```

## Key Commands
- `task setup` - Setup virtual environment and dependencies
- `task check` - Run all checks (lint + type-check + test) - MUST PASS before committing
- `task test` - Run tests
- `task lint` - Run linters (ruff check and format)
- `task lint-fix` - Run linters and fix issues
- `task type-check` - Run type checking (mypy)

## CLI Commands
- `cospec init` - Initialize a new project
- `cospec review` - Analyze codebase for inconsistencies
- `cospec hear` - Interactive hearing to resolve ambiguities
- `cospec test-gen` - Generate test cases from specifications