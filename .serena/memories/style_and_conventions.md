# cospec Code Style and Conventions

## Python Style Guidelines

### Type Safety
- **Use Pydantic models** for data structures
- **Avoid Any types** - prefer specific type annotations
- **Use strong typing** throughout the codebase
- **Type hints required** for all function parameters and return values

### Documentation
- **Write docstrings** before implementation
- **Use Google-style docstrings** for functions and classes
- **Update SPEC.md** when adding new features
- **Maintain BLUEPRINT.md** for technical decisions

### Code Quality
- **Ruff configuration**: line-length=120, target-version=py310
- **MyPy strict mode**: warn_return_any=true, disallow_untyped_defs=true
- **Follow PEP 8** with Ruff enforcement
- **Import organization**: standard library → third party → local imports

### Testing Standards
- **Test-Driven Generation (TDG)** approach
- **Mock external dependencies** (HTTP, APIs)
- **Use pytest** with async support
- **Test coverage**: All public APIs must have tests

### File Organization
- **CLI entry point**: `src/cospec/main.py` (typer-based)
- **Agents**: `src/cospec/agents/` (AI agent implementations)
- **Core functionality**: `src/cospec/core/` (analyzer, config)
- **Tests**: `tests/` directory with pytest structure

### Naming Conventions
- **snake_case** for functions and variables
- **PascalCase** for classes
- **UPPER_CASE** for constants
- **Descriptive names** that clearly indicate purpose

### Error Handling
- **Use specific exceptions** rather than generic ones
- **Provide helpful error messages** for CLI users
- **Graceful degradation** for optional features

### Configuration Management
- **Use Pydantic Settings** for configuration
- **Environment variables** for sensitive or environment-specific settings
- **Default values** for optional configuration