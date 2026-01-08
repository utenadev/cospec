# cospec Guidelines and Best Practices

## Development Guidelines

### Design Philosophy (`.rules/GuidlineDesign.md`)
- **Why rules exist** - Understanding the reasoning behind conventions
- **Design patterns** - Consistent architectural approaches
- **Philosophy documentation** - Ensure all decisions align with core principles

### Development Workflow (`.rules/GuidlineBasicRule.md`)
- **Human-AI collaboration workflow** - Standardized interaction patterns
- **Quality gates** - `task check` as mandatory validation
- **Communication protocols** - How AI and humans interact

### Coding Standards (`.rules/GuidlineCodingTesting.md`)
- **Code quality requirements** - Type safety, testing, documentation
- **Testing philosophy** - Test-Driven Generation approach
- **Code review standards** - Consistency and quality expectations

## Communication Guidelines

### Language Policy
- **User interaction**: All conversations in Japanese
- **Code comments**: English for international standards
- **Documentation**: English for source code, Japanese for user docs when specified
- **Commit messages**: English for consistency

### Development Communication
- **AI provides options** - Present multiple approaches with Pros/Cons
- **Human decision making** - Final choices remain with developers
- **Transparent reasoning** - Document why decisions were made

## Quality Assurance Standards

### Code Quality
- **Type safety first** - Use specific types, avoid Any
- **Strong typing throughout** - Pydantic models for data structures
- **Linting compliance** - ruff configuration with line-length=120
- **Type checking** - mypy with strict settings

### Testing Standards
- **Test-Driven Generation** - Generate tests from specifications
- **Mock external dependencies** - Isolate unit tests from external services
- **Async test support** - Use pytest-asyncio for async functionality
- **Coverage requirements** - All public APIs must have tests

### Documentation Standards
- **Living documentation** - Keep docs in sync with code
- **Single source of truth** - Avoid duplicate information
- **Clear specifications** - SPEC.md as the functional requirements baseline
- **Technical decisions** - BLUEPRINT.md for architectural choices

## Project Management

### Task Management
- **PLAN.md** - Implementation checklists and task tracking
- **WorkingLog.md** - Development history and completed work
- **Task validation** - Ensure requirements match specifications

### Version Control
- **Feature branches** - Isolate changes in separate branches
- **Meaningful commits** - Clear, descriptive commit messages in English
- **Review process** - Use `cospec review` for consistency checks
- **Merge strategy** - Ensure all checks pass before merging

## External Dependencies

### Required Tools
- **AI-Agent CLI tools**: Qwen, Opencode, Crush, MistralVibe, Gemini-CLI
- **Development tools**: go-task, pytest, ruff, mypy
- **Python dependencies**: typer, rich, pydantic-settings, openai

### Tool Configuration
- **Environment variables** for sensitive settings
- **pyproject.toml** for Python project configuration
- **Taskfile.yml** for cross-language task automation

## Troubleshooting

### Common Issues
- **ModuleNotFoundError**: Ensure virtual environment is activated
- **External tool errors**: Verify AI-Agent CLI tools are installed and in PATH
- **Linting failures**: Use `task lint-fix` to automatically fix style issues
- **Type errors**: Review mypy output and add proper type annotations

### Debug Commands
```bash
# Check Python environment
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