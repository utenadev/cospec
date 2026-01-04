# cospec

Collaborative Specification CLI - A platform where humans and AI agents work together to build high-quality software.

## Overview

`cospec` follows a "Doc-as-Context" and "Consistency-First" philosophy. It ensures that your code reflects your specifications and that decisions are made through clear trade-off analysis.

## Key Features (Planned)

- `cospec init`: Initialize a new project with the recommended structure.
- `cospec hear`: Interactive hearing to resolve ambiguities in `SPEC.md`.
- `cospec test-gen`: Generate test cases from specifications.
- `cospec review`: Analyze the codebase for inconsistencies.

## Tech Stack

- **Python**: Core logic
- **Typer**: CLI interface
- **Rich**: Terminal UI
- **Pydantic**: Data validation and settings

## Getting Started

### Prerequisites

- Python 3.10+
- [go-task](https://taskfile.dev/) (optional, but recommended)

### Setup

```bash
task setup
```

### Usage

```bash
# Show help
cospec --help
```
