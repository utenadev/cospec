# cospec Architecture Overview

## Core Components

### CLI Entry Point
- **File**: `src/cospec/main.py`
- **Framework**: Typer-based CLI
- **Commands**:
  - `init` - Project initialization
  - `review` - Codebase consistency review
  - `hear` - Interactive requirement clarification
  - `test-gen` - Test case generation

### Agent Architecture
- **BaseAgent** (`src/cospec/agents/base.py`) - Base class for AI agent implementations
- **ReviewerAgent** (`src/cospec/agents/reviewer.py`) - Specialized agent for code reviews
- **HearerAgent** (`src/cospec/agents/hearer.py`) - Interactive requirement clarification
- **TestGeneratorAgent** (`src/cospec/agents/test_generator.py`) - Test case generation

### Core Functionality
- **ProjectAnalyzer** (`src/cospec/core/analyzer.py`) - Collects project context from docs and source code
- **CospecConfig** (`src/cospec/core/config.py`) - Configuration management with tool settings and language preferences

## External Tool Integration

### Supported Tools
- **Qwen** - AI coding assistant integration
- **Opencode** - Code analysis tool
- **Crush** - Code optimization tool
- **MistralVibe** - Code generation tool
- **Gemini-CLI** - Google's AI coding tool

### Integration Pattern
- **External tool execution** - Delegates intelligence to CLI tools
- **Context collection** - Automatically gathers relevant project context
- **Language-aware prompting** - Supports both Japanese and English responses

## Configuration Management

### Environment Variables
- `COSPEC_LANGUAGE=ja` - Response language (ja/en)
- `COSPEC_DEFAULT_TOOL=qwen` - Default review tool

### Configuration File
- **Location**: `pyproject.toml`
- **Management**: Pydantic Settings for validation
- **Features**: Tool settings, language preferences, project metadata

## Documentation-Driven Development

### Documentation Structure
- **`docs/SPEC.md`** - Functional requirements (the "What")
- **`docs/BLUEPRINT.md`** - Technical architecture (the "How")
- **`docs/PLAN.md`** - Implementation checklists
- **`docs/WorkingLog.md`** - Development history

### `.rules/` Directory
- **`OverviewDesignThinking.md`** - Design philosophy and patterns
- **`OverviewBasicRule.md`** - Human-AI協働開発の実践ワークフロー
- **`OverviewCodingTestingThinking.md`** - Coding and testing guidelines

## Development Workflow Integration

### Task Automation
- **Tool**: `go-task` for task automation
- **File**: `Taskfile.yml`
- **Tasks**: setup, test, lint, type-check, build, clean

### Quality Assurance Pipeline
1. **Linting** - ruff for code style
2. **Type Checking** - mypy for type safety
3. **Testing** - pytest for functionality
4. **Documentation Review** - cospec review for consistency

### Testing Strategy
- **Test-Driven Generation** - Auto-generate tests from specifications
- **Mock external dependencies** - Isolate unit tests
- **Integration tests** - Test CLI commands and agent interactions
- **Async support** - pytest-asyncio for async functionality

## Project Structure Philosophy

### "Codebase as Context"
- **Documentation is truth** - All AI context comes from project docs
- **Single source of truth** - Avoid duplicate information
- **Living documentation** - Docs evolve with codebase

### "Consistency First"
- **Pre-implementation validation** - Check docs vs code before coding
- **Automated consistency checks** - cospec review catches discrepancies
- **Iterative refinement** - Return to docs when issues found

### "Decision Support"
- **AI provides options** - Present multiple approaches with trade-offs
- **Human makes choices** - Final decisions remain with developers
- **Transparent reasoning** - Document why decisions were made